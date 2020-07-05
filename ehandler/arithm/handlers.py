from event.event_bus import event_handler
from event.event_hub import MsgEvent
from const.event_consts import EVENT_ARITHM_SUB, EVENT_ARITHM_ADD


@event_handler()
def handle_sub_result(event: MsgEvent):
    print('handle_sub_result handling event: {}'.format(event))
    if event.type == EVENT_ARITHM_SUB:
        print('Processing {}'.format(event))


@event_handler()
def handle_add_result(event: MsgEvent):
    print('handle_add_result handling event: {}'.format(event))
    if event.type == EVENT_ARITHM_ADD:
        print('Processing {}'.format(event))
