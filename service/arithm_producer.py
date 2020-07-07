from const.event_consts import EVENT_ARITHM_SUB
from event.event_bus import direct_hub

cnt = 0


def sub():
    global cnt
    print('Send sub event ...')
    cnt -= 1
    if not direct_hub.publish(EVENT_ARITHM_SUB, {'res': cnt}):
        print('Cannot publish event!!!')
    return cnt
