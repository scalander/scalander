### IMPORTS

# I have absolutely no clue why half of these are here
# from curses import can_change_color
# from distutils.log import error
# from fcntl import F_SEAL_SEAL
# from imp import init_builtin
# from tabnanny import check
import time  # necessary
import datetime  # necessary
import json  # necessary
import os  # necessary
# import math # necessary
# from operator import truediv
# from typing import List
# from typing_extensions import Self


### CLASSES

# Theodore will most likely modify these later

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

class Block:  # only really for me and maybe frontend?
    def __init__(self, start, end):
        self.start, self.end = start, end


### FUNCTIONS

# functions here generally call the one(s) directly above them

def commitment_check(commitment, meeting):  # if meeting and commitment intersect, return True
    return (meeting.start > commitment.start and meeting.start < commitment.end) or (meeting.end > commitment.start and meeting.end < commitment.end)

def check_user_commits(meeting, user):  # check all the user's commitments with a meeting, return True if meeting time works
    for c in user.commitments:
        if commitment_check(c, meeting):
            return False
    return True  # add isAbsolute functionality to commitments later

def check_user_subs(meeting, user):  # check all the user's meeting subscriptions with a meeting, return True if meeting time works
    for c in user.meetingSubscriptions:
        if commitment_check(c.meeting, meeting):
            return False
    return True  # maybe add lockInDate functionality later?

def check_both(meeting, user):  # check both subs and commits, return True if it still works
    return check_user_commits(meeting, user) and check_user_subs(meeting, user)

def check_multiple_users(meeting, users):
    can, cannot = [], []
    for u in range(len(users)):
        if check_both(meeting, users[u]):
            can.append(u)
        else:
            cannot.append(u)
    return [can, cannot]

def check_all_times(times, users):  # times is a list of the meeting object (not rly efficient but whatever)
    return list(map(lambda t: check_multiple_users(t, users), times))

def chunk_times(times, users):
    arr = check_all_times(times, users)  # len(times) and len(arr) are equal
    chunks = []
    for i in range(len(arr)):
        if i == 0:  # start off the chunks with index 0
            chunks.append([times[i].start, None, arr[0][0], arr[0][1]])
            continue
        if not arr[i] == arr[i-1]:  # if the current index's list of available users is different from the last, end current chunk and start a new one
            chunks[-1][1] = times[i-1].end
            chunks.append([times[i].start, None, arr[i][0], arr[i][1]])
    chunks[-1][1] = times[-1].end
    return chunks  # chunks are structured as such: [start, end, [userIndex, ...], [userIndex, ...]]; first array is those who can make the meeting and second is those who cannot

def reduce_chunks(times, attendees, minChunks):
    chunks, chunkmap = chunk_times(times, list(map(lambda a: a.user, attendees))), []  # attendees is a list of the MeetingAttendee model, user is a child
    for i in range(len(chunks)):  # chunkmap format is as such: [[chunkIndex, value], ...]
        shouldContinue = False
        for j in i[3]:
            if attendees[j].isCritical:
                shouldContinue = True
                break
        if shouldContinue:
            continue
        value = 0
        for j in i[2]:
            if not attendees[j].isCritical:
                value += attendees[j].weight
        chunkmap.append([i, value])
    while len(chunkmap) > minChunks:  # chunkmap could potentially return less than minChunks values, which is fine
        # should maybe add a loop count limit to prevent crash abuse once I figure out errors
        indvalue, ind = chunkmap[0][1], 0
        for i in range(1, len(chunkmap)):
            if chunkmap[i][1] < indvalue:
                indvalue = chunkmap[i][1]
                ind = chunkmap[i][0]
        chunkmap.pop(ind)
    return list(map(lambda c: chunks[c[0]], chunkmap))  # return the chunks as specified in the chunkmap indexes

def if_neg(n):  # return 1 if the number is negative (basically if it crosses months I have to return one because it crosses days, else return the normal so it does whatever it normally would do)
    if n < 0:
        return 1
    else:
        return n

def create_times(blocks, meetingLength, meetingLockInDate, attendees, minChunks, timeIncrement, meetingName=""):  # timeIncrement is the increment between start times in minutes (>1), meetingLength is the length of the meeting in minutes (>1), meetingName is unnecessary
    # this is all under the assumption of <12h blocks, but will still work as long as they are under 24 hours
    chunks = []
    for i in blocks:
        times = []
        # meetingLength must be less than blockLen
        blockLen = i.end.minute - i.start.minute + (i.end.hour - i.start.hour) * 60 + if_neg(i.end.day - i.start.day) * 60 * 24  # I still have to make this work over months and years
        # if meetingLength > blockLen: return -1  # figure out a way to throw errors later
        timeQuantity = (blockLen - meetingLength) // timeIncrement + 1
        for j in range(timeQuantity):  # go through the block and add a time every time increment
            times.append(Meeting(meetingName, i.start + datetime.timedelta(minutes=timeIncrement*j), i.start + datetime.timedelta(minutes=meetingLength+timeIncrement*j), attendees, meetingLockInDate))  # change Meeting class later once we standardize the classes
        chunks += reduce_chunks(times, attendees, minChunks)
    return chunks

iBlocks = []
iMeetingLength = 45
iMeetingLockInDate = datetime.datetime.now()
iAttendees = []
iMinChunks = 5
iTimeIncrement = 5

print(create_times())