from django.db import models
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

class Commitment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_absolute = models.BooleanField()

class Meeting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    start = models.DateTimeField()
    end = models.DateTimeField()
    length = models.IntegerField()
    lock_in_date = models.DateTimeField()

class MeetingTimeProposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meeting = models.ForeignKey(Meeting, null=True, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    optimality = models.IntegerField()

class UserMeetingSubscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, null=True, on_delete=models.CASCADE)
    is_critical = models.BooleanField()
    weight = models.IntegerField()

class MeetingProposalAttendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proposal = models.ForeignKey(MeetingTimeProposal, null=True, on_delete=models.CASCADE)
    user_subscription = models.ForeignKey(UserMeetingSubscription, null=True, on_delete=models.CASCADE)
    is_committed = models.BooleanField()
