import time

from const.event_consts import EVENT_ARITHM_ADD
from event.event_bus import direct_hub, celery


@celery.task
def add():
    print('Async task triggered ...')
    time.sleep(3)
    direct_hub.publish(EVENT_ARITHM_ADD, {'res': 2})
