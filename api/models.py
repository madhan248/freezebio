from django.db import models
from django.contrib.auth.models import AbstractUser,User
from jsonfield import JSONField
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime

DEVICETYPE = (
    ('1','Cooling'),
    ('2','Heating')
)


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='users')
    number = PhoneNumberField(blank=True)
    organization = models.CharField(max_length=15,default="",blank=True,null=True)
    designation = models.CharField(max_length=15,default="",blank=True,null=True)
    verified = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    Dob = models.DateField(blank=True,null=True)
    
    def __str__(self):
        return "{0}-{1}-{2}".format(self.user.username,self.designation,self.organization)


class DeviceType(models.Model):
    device_type = models.CharField(max_length=100, default="", blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.device_type)

class DeviceConfiguration(models.Model):
    device_type = models.ForeignKey(DeviceType,on_delete=models.CASCADE,related_name="type")
    device_id = models.CharField(max_length=150, default="", blank=True, null=True)
    location = models.CharField(max_length=150,default="",blank=True,null=True)
    device_name = models.CharField(max_length=150,default="",blank=True,null=True)
    display = models.BooleanField(default=True)
    params = JSONField(default=[])
    device = models.CharField(choices=DEVICETYPE,default = '1',max_length=10)
    max_limit = models.FloatField(max_length=15,default=0.0)
    min_limit = models.FloatField(max_length=15,default=0.0)
    interval = models.CharField(max_length=15,default="1",blank=True,null=True)
    points = models.IntegerField()

    def __str__(self):
        return "{0}-{1}".format(self.device_type.device_type,self.device_id)
    
class DevicePermission(models.Model):
    device_config = models.ForeignKey(DeviceConfiguration, on_delete=models.CASCADE,related_name="config")
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name="profiles")

    def __str__(self):
        return "{0}-{1}".format(self.profile.username,self.device_config.device_id)
    
class LatestData(models.Model):
    device_type = models.CharField(max_length=150, default="", blank=True, null=True)
    device_id = models.CharField(max_length=15, default="", blank=True, null=True)
    data = JSONField(default={})
    timestamp = models.PositiveIntegerField()

    def __str__(self):
        return "{0}-{1}-{2}-{3}".format(self.device_id, self.timestamp,self.device_type, self.data)

class Events(models.Model):
    event_id = models.CharField(max_length=15, default="", blank=True, null=True)
    open_timestamp = models.PositiveIntegerField()
    closed_timestamp = models.PositiveIntegerField()
    event_count = models.CharField(max_length=15, default="", blank=True, null=True)
    device_id = models.CharField(max_length=15, default="", blank=True, null=True)
    acknowledged = models.TextField(default="")
    event_status = models.CharField(max_length=15, default="", blank=True, null=True)
    event_type = models.CharField(max_length=15, default="", blank=True, null=True)

    def __str__(self):
        return "{0}-{1}-{2}-{3}".format(self.event_id,self.device_id,self.event_status,self.acknowledged)

class Player(models.Model):
    player_id = models.CharField(max_length=100, default="", blank=True, null=True)
    profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return "{0}-{1}".format(self.player_id,self.profile.username)


class DeviceDataManager(models.QuerySet):
    
    def data_query_set(self,device_id,query_start,query_end):
        return self.filter(device_id=device_id,timestamp__gte=int(query_start),timestamp__lte=int(query_end))
    
    def latest_query_set(self,device_id):
        return self.filter(device_id=device_id).first()


class DeviceData(models.Model):
    device_type = models.CharField(max_length=150, default="", blank=True, null=True)
    device_id = models.CharField(max_length=15, default="", blank=True, null=True)
    data = JSONField(default={})
    timestamp = models.PositiveIntegerField()
    objects = models.Manager()
    data_objects = DeviceDataManager.as_manager()

    class Meta:
        indexes = [models.Index(fields=['device_id', '-timestamp',]), ]

    def __str__(self):
        return "{0}-{1}-{2}-{3}".format(self.device_id,self.timestamp,self.device_type,self.data)


class ServiceModel(models.Model):
    task = models.CharField(max_length=150, default="", blank=True, null=True)
    timestamp = models.CharField(max_length=150, default="", blank=True, null=True)
    service = models.CharField(max_length=150, default="", blank=True, null=True)

    def __str__(self):
        return "{0}-{1}-{2}".format(self.task,self.timestamp,self.service)
