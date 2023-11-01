from django.db import models
from django.contrib.auth.models import User
import datetime
import pytz
# Create your models here.

class attendee(models.Model):
    id = models.CharField(max_length=20,primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    isCash = models.BooleanField()
    handledBy = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    hashVal = models.CharField(max_length=64)
    isVip = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(default=(datetime.datetime.now()+datetime.timedelta(hours=5,minutes=30)).isoformat(' '))
