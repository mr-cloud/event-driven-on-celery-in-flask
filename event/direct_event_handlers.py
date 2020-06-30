from event.event_hub import MsgEvent


def on_add_direct(event: MsgEvent):
    from service.arithm_consumer import handle_add_result
    handle_add_result(event)
