from django.db import models

class User(models.model):
    name = models.CharField()

class Commitment(models.model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_absolute = models.BooleanField()

class Meeting(models.model):
    name = models.CharField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    lock_in_duration = models.DurationField()

class UserMeetingSubscription(models.model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    meeting = models.ForeignKey(Meeting, on_delete=models.DO_NOTHING)
    is_critical = models.BooleanField()
    weight = models.IntegerField()

# Create your models here.
