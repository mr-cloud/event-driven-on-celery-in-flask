import threading
import uuid
from threading import Thread
from typing import Callable

import kombu
from kombu import Connection
from kombu.mixins import ConsumerMixin
from kombu.pools import connections, producers

# setting consumer class
from event import handler_register
from event.messages import MsgEvent
from event.transports import ETransport
from event.utils import dynamic_import_from_src


class C(ConsumerMixin):
    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_msg],
                         accept=['json', 'pickle'])]

    def __init__(self, connection, queues: list, handler: Callable) -> None:
        print('C Threading: ', threading.current_thread().getName())
        print('#C# id=', id(self))
        self.connection = connection
        self.queues = queues
        self.handler = handler

    def on_msg(self, body, message):
        print('#C# on_msg Threading: ', threading.current_thread().getName())
        print('I have received message: {0!r}, type: {1}'.format(body, type(body)))
        self.handler(body)
        message.ack()
        print('Acked msg', message)

    def on_connection_revived(self):
        print('#C# on_connection_revived')
        super().on_connection_revived()

    def on_consume_ready(self, connection, channel, consumers, **kwargs):
        print('#C# on_consume_ready')
        super().on_consume_ready(connection, channel, consumers, **kwargs)

    def on_connection_error(self, exc, interval):
        print('#C# on_connection_error')
        super().on_connection_error(exc, interval)

    def extra_context(self, connection, channel):
        print('#C# extra_context')
        return super().extra_context(connection, channel)

    def run(self, _tokens=1, **kwargs):
        print('#C# run Threading: ', threading.current_thread().getName())
        super().run(_tokens, **kwargs)

    def establish_connection(self):
        print('#C# establish_connection')
        return super().establish_connection()


class EventHub(Thread):
    """
    :param url: or use connection URL
    :param transport: exchange type
    :param rkey: routing key
    """

    def __init__(self, exchange: str, transport: str, rkey: str, url: str, scan_paths=None) -> None:
        Thread.__init__(self)
        self.rkey = rkey
        self.transport = transport
        self.exchange = exchange
        self.conn = Connection(url)
        # self.conn_pool = connections[conn]
        # self.producer_pool = producers[conn]
        scan_paths = [] if not scan_paths else scan_paths
        for p in scan_paths:
            dynamic_import_from_src(p)
        self.handlers = handler_register.ehandlers
        pass

    def _handle(self, event: MsgEvent):
        print('#handlers=%s' % [(k, len(v)) for k, v in self.handlers.items()])
        if not (event.type in self.handlers):
            print('#drain-event# event-type=%s' % event.type)
        else:
            for h in self.handlers[event.type]:
                h(event)

    def publish(self, mtype: str, msg: str) -> bool:
        """
        :param mtype: msg type
        :param msg: payload in event in json string
        """
        print('publishing type={}, msg={}'.format(mtype, msg))
        try:
            with producers[self.conn].acquire(block=True) as producer:
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

    def _hub_bootstrap(self):
        with connections[self.conn].acquire(block=True) as conn:
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
            # It will run forever to consume msg.
            C(conn, [queue], self._handle).run()

    def run(self) -> None:
        print('Thread %s: starting run' % threading.current_thread().getName())
        self._hub_bootstrap()
