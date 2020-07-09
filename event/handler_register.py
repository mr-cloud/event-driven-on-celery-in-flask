from collections import defaultdict

ehandlers = defaultdict(list)


def register(etype: str):
    """
    :param etype: event type
    """
    def h(func):
        print('Registering event handler: %s::%s' % (func.__module__, func.__name__))
        ehandlers[etype].append(func)
        return func
    return h
