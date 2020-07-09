import time

from celery_setup import celery
from const.event_consts import EVENT_ARITHM_ADD
from event_bus import direct_hub


@celery.task
def add_async(a: int, b: int):
    """Never read/write on global vars cause newly booted worker would lost it."""
    print('Async task triggered ...')
    time.sleep(1)
    if not direct_hub.publish(EVENT_ARITHM_ADD, {'res': a+b}):
        print('Cannot publish event!!!')

