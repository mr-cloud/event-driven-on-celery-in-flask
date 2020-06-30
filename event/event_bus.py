import inspect
import os
import sys

from celery import Celery

from event import direct_event_handlers
from event.event_hub import EventHub, ETransport


config = dict(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

celery = Celery('event bus', broker=config['CELERY_BROKER_URL'])
celery.conf.update(config)

ext_path = [os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'task')]
print(ext_path)
sys.path.extend(ext_path)
celery.autodiscover_tasks(packages=['task.arithm'])

direct_hub = EventHub(celery, 'async-channel', ETransport.DIRECT, 'p2p-routing')


def event_handler(ttype: ETransport = ETransport.DIRECT):
    def h(func):
        print('Registering event handler: %s::%s' % (func.__module__, func.__name__))
        if ttype == ETransport.DIRECT:
            direct_hub.register_handler(func)
        return func
    return h


direct_handlers = [fn for name, fn in inspect.getmembers(direct_event_handlers, inspect.isfunction)]
for h in direct_handlers:
    direct_hub.register_handler(h)
