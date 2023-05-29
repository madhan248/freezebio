from datetime import datetime
from celery import shared_task
from .models import ServiceModel

@shared_task
def helloworld():
	print("Hello World")
	c = ServiceModel(task="helloworld",timestamp=datetime.now(),service="Celery")
	c.save()

# @shared_task
# def sample_task():
# 	print("from celery.tasks sample_task: {}".format(datetime.now()))
# 	return True


# @shared_task
# def send_email_report():
# 	print("from celery.tasks send_email_report: {}".format(datetime.now()))
# 	return True

# celery.current_app.conf.beat_schedule = {
#     "helloworld": {
#         "task": "helloworld",
#         "schedule": crontab(minute="*/1"),
#     },
#     }