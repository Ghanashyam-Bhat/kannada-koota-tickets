from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
# Create your models here.


class UTC530DateTimeField(models.DateTimeField):
    def get_default(self):
        return timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))

class attendee(models.Model):
    id = models.CharField(max_length=20,primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    isCash = models.BooleanField()
    handledBy = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    hashVal = models.CharField(max_length=64)
    isVip = models.BooleanField(default=False)
    created_at = UTC530DateTimeField(default=timezone.now)