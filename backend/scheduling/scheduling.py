# IMPORTS
from curses import can_change_color
from distutils.log import error
from fcntl import F_SEAL_SEAL
<<<<<<< HEAD
=======
from imp import init_builtin
from tabnanny import check
>>>>>>> f549312 (classes added)
import time
from operator import truediv
from typing import List
from typing_extensions import Self

# CLASSES
class User:
    def __init__(self, name, commitments, meetingSubscriptions):
        self.name, self.commitments, self.meetingSubscriptions = name, commitments, meetingSubscriptions

class Commitment:
    def __init__(self, start, end, isAbsolute):
        self.start, self.end, self.isAbsolute = start, end, isAbsolute

class Meeting:
    def __init__(self, name, start, end, subscribedUsers, lockInDate):
        self.name, self.start, self.end, self.subscribedUsers, self.lockInDate = name, start, end, subscribedUsers, lockInDate

class MeetingAttendee:
    def __init__(self, user, isCritical, weight):
        self.user, self.isCritical, self.weight = user, isCritical, weight
class UserAttendence:
    def __init__(self, meeting, isCritical, weight):
        self.meeting, self.isCritical, self.weight = meeting, isCritical, weight


# FUNCTIONS
def commitment_check(commitment, meeting):  # if meeting and commitment intersect, return True
    return (meeting.start > commitment.start and meeting.start < commitment.end) or (meeting.end > commitment.start and meeting.end < commitment.end)

def check_user_commits(meeting, user):  # check all the user's commitments with a meeting, return True if meeting time works
    for c in user.commitments:
        if commitment_check(c, meeting):
            return False
    return True

def check_user_subs(meeting, user):  # check all the user's meeting subscriptions with a meeting, return True if meeting time works
    for c in user.meetingSubscriptions:
        if commitment_check(c.meeting, meeting):
            return False
    return True

def check_both(meeting, user):  # check both subs and commits, return True if it still works
    return check_user_commits(meeting, user) and check_user_subs(meeting, user)

def checkMultipleUsers(meeting, users):
    can, cannot = [], []
    for u in range(len(users)):
        if check_both(meeting, users[u]):
            can.append(u)
        else:
            cannot.append(u)
    return [can, cannot]

def checkAllTimes(times, users):
    return list(map(lambda t: checkMultipleUsers(t, users), times))

def returnTopTimes(times, users):
    arr = checkAllTimes(times, users)
