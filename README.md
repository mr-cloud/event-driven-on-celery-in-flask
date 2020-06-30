Using Celery with Flask
=======================
Event-driven based on Celery + Kombu in Flask.

Quick Setup
-----------

1. Open a second terminal window and start a local Redis server (if you are on Linux or Mac, execute `run-redis.sh` to install and launch a private copy).
2. Start a Celery worker: `celery worker -A  --loglevel=info`.
3. Start the Flask application on your original terminal window: `celery worker -A event.event_bus --loglevel=info`.
4. Go to `http://localhost:5001/` and refer to end-points in app.py. Enjoy this application!

How to develop
--------------
- Async task. `task/arithm/tasks.py::add` for async-task and producer. `add()` should be decorated by `@celery.task` 
    and called with `apply_async()`. `service/arithm_consumer.py::handle_add_result` for consumer.
    `handle_add_result()` should also be put under handler module `event/direct_event_handlers.py` and it will be registered
    automatically in the *event_bus* `event/event_bus.py` via inspection.
- Event publish and consuming. `service/arithm_producer.py::sub` for producer .`service/arithm_consumer.py::handle_sub_result` for consumer.
     `handle_sub_result` just needs to be decorated by `@event_handler()` and it will be registered automatically.

Reference
----------
- [1] For details on how this all works, see article [Using Celery with Flask](http://blog.miguelgrinberg.com/post/using-celery-with-flask).
