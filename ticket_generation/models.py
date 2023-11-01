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
    created_at = models.DateTimeField(default=(datetime.datetime.now().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))).isoformat(' '))



# Get the current date and time
current_datetime = datetime.datetime.now()

# Define a timedelta for 5 hours and 30 minutes
time_delta = datetime.timedelta(hours=5, minutes=30)

# Add the timedelta to the current datetime
new_datetime = current_datetime + time_delta