from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms

# mongoengine
from mongoengine import *
connect('mytestdb', host='10.101.100.95', port=27017)
# Create your models here.

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    office_hours = models.TimeField()
    off_hours = models.TimeField()
    clockin_time = models.TimeField(blank=True, null=True)
    clockout_time = models.TimeField(blank=True, null=True)
    clockin_status = models.CharField(max_length=20)
    clockout_status = models.CharField(max_length=20)
    total_working_hours = models.FloatField()
    abnormal_hours = models.FloatField()


    def __str__(self):
        return f"{self.user.username}'s Attendance"

class MongoEngineUsers(Document):
     username=StringField(required=True)             # field defined in mongoengine
     email=StringField(required=True)
    #  last_update = DateTimeField(required=True)