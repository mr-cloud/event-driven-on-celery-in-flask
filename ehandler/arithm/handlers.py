from const.event_consts import EVENT_ARITHM_SUB, EVENT_ARITHM_ADD
from event.handler_register import register
from event.messages import MsgEvent

print('importing', __file__)


@register(etype=EVENT_ARITHM_SUB)
def handle_sub_result(event: MsgEvent):
    print('handle_sub_result handling event: {}'.format(event))
    print('Processing {}'.format(event))


@register(etype=EVENT_ARITHM_ADD)
def handle_add_result(event: MsgEvent):
    print('handle_add_result handling event: {}'.format(event))
    print('Processing {}'.format(event))
