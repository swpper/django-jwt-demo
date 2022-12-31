from typing import Any
from datetime import datetime, timezone, timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser, User


class ResourceId(models.TextChoices):
    '''value, label'''
    WEATHER_FORECAST = 'wf', 'weather_forecast'
    LTNG_FORECAST = 'lf', 'ltng_forecast'

# class Scope(models.TextChoices):
#     '''value, label'''
#     READ = 'r', 'read'
#     WRITE = 'w', 'write'


class Customer(AbstractUser):
        
    # username = models.CharField(max_length=50, primary_key=True)
    # password = models.CharField(max_length=100)
    resource_name = models.CharField(max_length=50, verbose_name='资源权限')   # JSON-serialized  list
    scope = models.CharField(max_length=50, verbose_name='scope')    # JSON-serialized  list
    update_date = models.DateTimeField('update date',
        default=datetime(1970,1,1,0, tzinfo=timezone(timedelta(hours=0))))


    def __str__(self):
        return self.username


class Resource(models.Model):
    resource_name = models.CharField(max_length=10, primary_key=True)
    resource_secret = models.CharField(max_length=100)
    update_date = models.DateTimeField('update date')

    def __str__(self):
        return self.resource_name




