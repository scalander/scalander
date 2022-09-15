from django.db import models

class User(models.Model):
    name = models.CharField(max_length=64)

class Commitment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_absolute = models.BooleanField()

class Meeting(models.Model):
    name = models.CharField(max_length=256)
    start = models.DateTimeField()
    end = models.DateTimeField()
    lock_in_duration = models.DurationField()

class MeetingTimeProposal(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.DO_NOTHING)
    start = models.DateField()
    end = models.DateField()
    optimality = models.IntegerField()

class UserMeetingSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    meeting = models.ForeignKey(Meeting, on_delete=models.DO_NOTHING)
    is_critical = models.BooleanField()
    weight = models.IntegerField()

class MeetingProposalAttendance(models.Model):
    proposal = models.ForeignKey(MeetingTimeProposal, on_delete=models.DO_NOTHING)
    user_subscription = models.ForeignKey(UserMeetingSubscription, on_delete=models.DO_NOTHING)
    is_committed = models.BooleanField()