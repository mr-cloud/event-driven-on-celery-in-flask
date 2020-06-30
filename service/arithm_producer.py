from const.event_consts import EVENT_ARITHM_SUB
from event.event_bus import direct_hub


def sub():
    print('Send sub event ...')
    res = -1
    direct_hub.publish(EVENT_ARITHM_SUB, {'res': res})
    return res
