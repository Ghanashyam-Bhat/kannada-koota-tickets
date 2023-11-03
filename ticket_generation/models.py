from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class attendee(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=100)
    isCash = models.BooleanField()
    handledBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    hashVal = models.CharField(max_length=64)
    isVip = models.BooleanField(default=False)
    created_datetime = models.DateTimeField()
