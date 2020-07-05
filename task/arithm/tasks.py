import time

from const.event_consts import EVENT_ARITHM_ADD
from event.event_bus import direct_hub, celery


@celery.task
def add(a: int, b: int):
    """Never read/write on global vars cause newly booted worker would lost it."""
    print('Async task triggered ...')
    time.sleep(1)
    direct_hub.publish(EVENT_ARITHM_ADD, {'res': a+b})
