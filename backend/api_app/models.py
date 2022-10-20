from django.db import models

class User(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

class Commitment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_absolute = models.BooleanField()

class Meeting(models.Model):
    name = models.CharField(max_length=256)
    start = models.DateTimeField()
    end = models.DateTimeField()
    lock_in_date = models.DateTimeField()

class MeetingTimeProposal(models.Model):
    meeting = models.ForeignKey(Meeting, null=True, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    optimality = models.IntegerField()

class UserMeetingSubscription(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, null=True, on_delete=models.CASCADE)
    is_critical = models.BooleanField()
    weight = models.IntegerField()

class MeetingProposalAttendance(models.Model):
    proposal = models.ForeignKey(MeetingTimeProposal, null=True, on_delete=models.DO_NOTHING)
    user_subscription = models.ForeignKey(UserMeetingSubscription, null=True, on_delete=models.DO_NOTHING)
    is_committed = models.BooleanField()
