# IMPORTS

from curses import can_change_color
from distutils.log import error
from fcntl import F_SEAL_SEAL
from imp import init_builtin
from tabnanny import check
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

def check_multiple_users(meeting, users):
    can = []
    # cannot = []
    for u in range(len(users)):
        if check_both(meeting, users[u]):
            can.append(u)
        # else:
        #     cannot.append(u)
    return can

def check_all_times(times, users):
    return list(map(lambda t: check_multiple_users(t, users), times))

def chunk_times(times, users):
    arr = check_all_times(times, users)  # len(times) and len(arr) are equal
    chunks = []
    for i in range(len(arr)):
        if i == 0:  # start off the chunks with index 0
            chunks.append([times[i].start, None, arr[0]])
            continue
        if not arr[i] == arr[i-1]:  # if the current index's list of available users is different from the last, end current chunk and start a new one
            chunks[-1][1] = times[i-1].end
            chunks.append([times[i].start, None, arr[i]])
    chunks[-1][1] = times[-1].end
    return chunks  # chunks are structured as such: [start, end, [userIndex,...]]

def reduce_chunks(times, users, minUsers):  # minUsers is the minimum amount of users that will be considered as an option
    return list(filter(lambda c: len(c[2]) >= minUsers, chunk_times(times, users)))

def create_times(blocks, users, minUsers):
    pass