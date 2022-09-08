# IMPORTS
from curses import can_change_color
from distutils.log import error
from fcntl import F_SEAL_SEAL
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

class UserMeetingSubscription:
    def __init__(self, parent, user, meeting, isCritical, weight):
        if parent is Meeting:
            self.user = user
        elif parent is User:
            self.meeting, self.isCritical, self.weight = meeting, isCritical, weight
        else:
            error("Please specific parent class")


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

def checkBoth(meeting, user): #check both subs and commits, return True if it still works
    return (checkUserCommits(meeting, user) and checkUserSubs(meeting, user))
