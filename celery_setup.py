import os
import sys

from celery import Celery

config = dict(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

celery = Celery('async-task-celery', broker=config['CELERY_BROKER_URL'])
celery.conf.update(config)

ext_path = [os.path.dirname(os.path.abspath(__file__)),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'task')]

print(ext_path)
sys.path.extend(ext_path)
celery.autodiscover_tasks(packages=['task.arithm'])
