Using Celery with Flask
=======================
Event-driven based on Celery + Kombu in Flask.

Quick Setup
-----------

1. Open a second terminal window and start a local Redis server (if you are on Linux or Mac, execute `run-redis.sh` to install and launch a private copy).
2. Start a Celery worker: `celery worker -A event.event_bus --loglevel=info`.
3. Start the Flask application on your original terminal window: `python app.py [<port numeber>]`.
4. Go to `http://localhost:5001/` and refer to end-points in app.py. Enjoy this application!

How to develop
--------------
- Async task. `task/arithm/tasks.py::add` for async-task and producer. `add()` should be decorated by `@celery.task` 
    and called with `apply_async()`. `ehandler/arithm/handlers.py::handle_add_result` for consumer. 
    New directory for async-task should be created under `task` and name must named as `tasks.py`, 
    then added into `event/event_bus.py` via `celery.autodiscover_tasks`. 
- Event publish and consuming. `service/arithm_producer.py::sub` for producer .`ehandler/arithm/handlers.py::handle_sub_result` for consumer.
     `handle_sub_result` just needs to be decorated by `@event_handler()` and it will be registered automatically.
    New directory for handler should be created under `ehandler` and name must named as `handlers.py`, 
    then added into `event/event_bus.py` via `celery.autodiscover_tasks`.
    
 
Reference
----------
- [1] For details on how this all works, see article [Using Celery with Flask](http://blog.miguelgrinberg.com/post/using-celery-with-flask).
