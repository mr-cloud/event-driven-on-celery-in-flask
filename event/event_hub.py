
# named_tuple
import uuid
from collections import namedtuple
from typing import Callable

import kombu

# payload in json string
MsgEvent = namedtuple('MsgEvent', ['id', 'type', 'payload'])


class ETransport(object):
    DIRECT = 'direct'


class EventHub:
    """
    :param app: engine like celery instance
    :param transport: exchange type
    :param rkey: routing key
    """
    def __init__(self, app, exchange: str, transport: str, rkey: str) -> None:
        self.rkey = rkey
        self.transport = transport
        self.exchange = exchange
        self.app = app
        self.handlers = []
        self._bootstrap()
        
    def _handle(self, event: MsgEvent):
        for h in self.handlers:
            h(event)
    
    def register_handler(self, h: Callable):
        self.handlers.append(h)

    def publish(self, mtype: str, msg: str) -> bool:
        """
        :param mtype: msg type
        :param msg: payload in event in json string
        """
        print('publishing type={}, msg={}'.format(mtype, msg))
        try:
            with self.app.producer_pool.acquire(block=True) as producer:
                producer.publish(MsgEvent(uuid.uuid4().hex, mtype, msg),
                                 exchange=self.exchange,
                                 routing_key=self.rkey,
                                 serializer='pickle',
                                 retry=True
                                 )
            return True
        except Exception as e:
            print(e)
            return False

    def _bootstrap(self):
        with self.app.pool.acquire(block=True) as conn:
            exchange = kombu.Exchange(
                name=self.exchange,
                type=self.transport,
                durable=True,
                channel=conn,
            )
            exchange.declare()
            if self.transport == ETransport.DIRECT:
                q = 'sameQ'
            queue = kombu.Queue(
                name=q,
                exchange=exchange,
                routing_key=self.rkey,
                channel=conn,
                message_ttl=600,
                queue_arguments={
                    'x-queue-type': 'classic'
                },
                durable=True
            )
            queue.declare()
            hub = self
            # setting consumer class
            from celery import bootsteps
            class MyConsumerStep(bootsteps.ConsumerStep):

                def get_consumers(self, channel):
                    # accept serializable
                    return [kombu.Consumer(channel,
                                           queues=[queue],
                                           callbacks=[self.handle_event],
                                           accept=['json', 'pickle'])]
        
                def handle_event(self, body, message):
                    print('I have received message: {0!r}, type: {1}'.format(body, type(body)))
                    hub._handle(body)
                    message.ack()
                    print('Acked msg', message)

            # Register the custom consumer
            self.app.steps['consumer'].add(MyConsumerStep)
