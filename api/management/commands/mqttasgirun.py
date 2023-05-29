from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import subprocess
import time

class Command(BaseCommand):
    help = 'Run Celery-workers,Celerybeats,Mqttasgi'

    def handle(self, *args, **kwargs):
        subprocess.Popen("gnome-terminal -- bash bashfiles/celeryworkers.sh", stdout=subprocess.PIPE,stderr=None,shell=True)
        subprocess.Popen("gnome-terminal -- bash bashfiles/mqttasgibash.sh", stdout=subprocess.PIPE,stderr=None,shell=True)
        time.sleep(5)
        subprocess.Popen("gnome-terminal -- bash bashfiles/celerybeats.sh", stdout=subprocess.PIPE,stderr=None,shell=True)
        subprocess.run(["python","manage.py","runserver","0.0.0.0:8000"])
        user = User.objects.count()
        if user == 0:
            superuser = User.objects.create_user(username="admin",email="admin@freezebio.com",password="admin@1",
                is_staff=True,is_active=True,is_superuser=True)