# from django.db import models
from djongo import models
from django import forms

# Create your models here.


# class PLCDB(models.Model):
#     csv_filename = models.CharField(max_length=30)
#     interval = models.FloatField()
#     device_name = models.CharField(max_length=30)
#     dB_name = models.CharField(max_length=30)
#     dB_size = models.PositiveSmallIntegerField(default=0)
#     endian = models.CharField(max_length=10)
#     dB_num = models.PositiveSmallIntegerField(default=0)

#     class Meta:
#         abstract = True


# class Device(models.Model):
#     slot = models.PositiveSmallIntegerField(default=1)
#     protocol = models.CharField(max_length=30)
#     Name = models.CharField(max_length=30)
#     ip = models.GenericIPAddressField(null=True)
#     pseudo = models.PositiveSmallIntegerField(default=0)
#     Rack = models.PositiveSmallIntegerField(default=0)

#     class Meta:
#         abstract = True


# class DB_list(models.Model):
#     # plc_dbs = models.ArrayModelField(
#     #     model_container=PLCDB,
#     # )

#     plc_dbs = models.EmbeddedModelField(
#         model_container=PLCDB,
#     )

# class Device_list(models.Model):
#     # devices = models.ArrayModelField(
#     #     model_container=Device,
#     # )

#     devices = models.EmbeddedModelField(
#         model_container=Device,
#     )


# class DB_Data(models.Model):
#     TimeStamp = models.DateTimeField()
#     DB = models.CharField(max_length=30)
#     valid = models.PositiveSmallIntegerField(default=0)
#     Device = models.CharField(max_length=30)
#     data = 