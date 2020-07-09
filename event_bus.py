import os

from event.event_hub import EventHub, ETransport

TRANSPORT_URL = 'redis://localhost:6379/0'

# P2P Load Balancing Event Hub.
direct_hub = EventHub('EventHub-direct', ETransport.DIRECT, 'p2p-routing', url=TRANSPORT_URL,
                      scan_paths=[os.path.join(os.path.dirname(__file__), 'ehandler')])
direct_hub.start()
print('Event bus launched.')

if __name__ == '__main__':
    pass
