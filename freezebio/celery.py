from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, shared_task
from django.conf import settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freezebio.settings')

app = Celery('freezebio')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))
  print('hello world')

from celery.schedules import crontab

# app.conf.beat_schedule = {
#     # Executes every Monday morning at 7:30 a.m.
#     'add-every-monday-morning': {
#         'task': 'tasks.add',
#         'schedule': crontab(hour=7, minute=30, day_of_week=1),
#         'args': (16, 16),
#     },
# }

app.conf.beat_schedule = {
    "helloworld": {
        "task": "api.tasks.helloworld",
        "schedule": crontab(minute="*/1"),
    },
    # "send_email_report": {
    #     "task": "api.tasks.send_email_report",
    #     "schedule": crontab(hour="*/1"),
    # },
}