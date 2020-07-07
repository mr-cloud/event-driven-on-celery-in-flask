import inspect
import os
import sys

from celery import Celery

from event.event_hub import EventHub, ETransport


config = dict(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

celery = Celery('event bus', broker=config['CELERY_BROKER_URL'])
celery.conf.update(config)

ext_path = [os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'task'),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ehandler')]
print(ext_path)
sys.path.extend(ext_path)
celery.autodiscover_tasks(packages=['task.arithm'])
celery.autodiscover_tasks(packages=['ehandler.arithm'], related_name='handlers')

# P2P Load Balancing Event Hub.
direct_hub = EventHub(celery, 'event-driven', ETransport.DIRECT, 'p2p-routing')


def event_handler(etype: str, ttype: ETransport = ETransport.DIRECT):
    """
    :param etype: event type
    :param ttype: transport type
    """
    def h(func):
        print('Registering event handler: %s::%s' % (func.__module__, func.__name__))
        if ttype == ETransport.DIRECT:
            direct_hub.register_handler(etype, func)
        return func
    return h

