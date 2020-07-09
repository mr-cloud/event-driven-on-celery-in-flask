from const.event_consts import EVENT_ARITHM_SUB, EVENT_ARITHM_UNCLAIMED
from event_bus import direct_hub
from task.arithm.tasks import add_async

cnt = 0


def sub():
    global cnt
    print('Send sub event ...')
    cnt -= 1
    if not direct_hub.publish(EVENT_ARITHM_SUB, {'res': cnt}):
        print('Cannot publish event!!!')
    return cnt


def add(a: int, b: int):
    add_async.delay(a, b)


def unclaimed_msg():
    if not direct_hub.publish(EVENT_ARITHM_UNCLAIMED, {'res': None}):
        print('Cannot publish event!!!')
