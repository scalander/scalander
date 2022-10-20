### EXPORTS

__all__ = ["main_scheduling", "reduce_chunks", "User", "Commitment", "Meeting", "MeetingAttendee", "UserAttendence", "Block", "BlockLengthError", "MeetingLengthError", "TimeIncrementError"]


### IMPORTS

import time
import datetime  # necessary
import json
import random
import os


### CLASSES

# Theodore will most likely modify these later

class User:
    def __init__(self, name, commitments, meetingSubscriptions, id):
        self.name, self.commitments, self.meetingSubscriptions, self.id = name, commitments, meetingSubscriptions, id  # id is apparently a 5 number string for now (I generate it in tests as 10000-99999)

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


### ERRORS

class BlockLengthError(Exception): pass  # one (or more) of the blocks is less in length than the meetingLength
class MeetingLengthError(Exception): pass  # meetingLength is less than 1 minute
class TimeIncrementError(Exception): pass  # timeIncrement is less than 1 minute


### FUNCTIONS

# functions here generally call the one(s) directly above them

def commitment_check(commitment, meeting):  # if meeting and commitment intersect, return True
    return (commitment.start < meeting.start < commitment.end) or (commitment.start < meeting.end < commitment.end) or (meeting.start <= commitment.start and commitment.end <= meeting.end)

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

def check_all_times(times, users):  # times is a list of the meeting object (not rly storage efficient but whatever)
    return [check_multiple_users(t, users) for t in times]

def chunk_times(times, users):
    arr = check_all_times(times, users)  # len(times) and len(arr) are equal
    chunks = [[times[0].start, None, arr[0][0], arr[0][1]]]
    for i in range(1, len(arr)):
        if not arr[i] == arr[i-1]:  # if the current index's list of available users is different from the last, end current chunk and start a new one
            chunks[-1][1] = times[i-1].end
            chunks.append([times[i].start, None, arr[i][0], arr[i][1]])
    chunks[-1][1] = times[-1].end
    return chunks  # chunks are structured as such: [start, end, [userIndex, ...], [userIndex, ...]]; first array is those who can make the meeting and second is those who cannot

# reduce_chunks used to be above create times but it caused chunks to not be reduced correctly

# def if_neg(n):  # return 1 if the number is negative (basically if it crosses months I have to return one because it crosses days, else return the normal so it does whatever it normally would do)
#     if n < 0:
#         return 1
#     else:
#         return n

def create_times(blocks, meetingLength, meetingLockInDate, attendees, timeIncrement, meetingName):  # timeIncrement is the increment between start times in minutes (>1), meetingLength is the length of the meeting in minutes (>1), meetingName is unnecessary; used to have a minChunks param between attendees and timeIncrement
    # this used to be all under the assumption of <12h blocks, but would still work as long as they are under 24 hours (BEFORE I CHANGED THE BLOCKLEN CALCULATION TO USE TIMEDELTA)
    if meetingLength < 1:
        raise MeetingLengthError
    if timeIncrement < 1:
        raise TimeIncrementError
    chunks = []
    for i in blocks:
        times = []
        # blockLen = i.end.minute - i.start.minute + (i.end.hour - i.start.hour) * 60 + if_neg(i.end.day - i.start.day) * 60 * 24
        blockLen = (i.end - i.start).total_seconds() // 60
        if meetingLength > blockLen: # meetingLength must be less than blockLen
            raise BlockLengthError
        timeQuantity = (blockLen - meetingLength) // timeIncrement + 1
        for j in range(int(timeQuantity)):  # go through the block and add a time every time increment
            times.append(Meeting(meetingName, i.start + datetime.timedelta(minutes=timeIncrement*j), i.start + datetime.timedelta(minutes=meetingLength+timeIncrement*j), attendees, meetingLockInDate))  # change Meeting class later once we standardize the classes
        chunks += chunk_times(times, [a.user for a in attendees])
    return chunks

def reduce_chunks(blocks, meetingLength, meetingLockInDate, attendees, minChunks, timeIncrement, meetingName=" "):
    chunks, chunkmap = create_times(blocks, meetingLength, meetingLockInDate, attendees, timeIncrement, meetingName), []  # attendees is a list of the MeetingAttendee model, user is a child, used to pass minChunks between attendees and timeIncrement
    for i in range(len(chunks)):  # chunkmap format is as such: [[chunkIndex, value], ...]
        # shouldContinue = False
        # for j in chunks[i][3]:
        #     if attendees[j].isCritical:
        #         shouldContinue = True
        #         break
        # if shouldContinue:
        #     continue
        class Critical(Exception): pass
        try:
            for j in chunks[i][3]:
                if attendees[j].isCritical:
                    raise Critical
        except Critical:
            continue
        value = 0
        for j in chunks[i][2]:
            if not attendees[j].isCritical:
                value += attendees[j].weight
        chunkmap.append([i, value])
    while len(chunkmap) > minChunks:  # chunkmap could potentially return less than minChunks values, which is fine
        # should maybe add a loop count limit to prevent crash abuse once I figure out errors
        indvalue, ind = chunkmap[0][1], 0
        for i in range(1, len(chunkmap)):
            if chunkmap[i][1] < indvalue:
                indvalue = chunkmap[i][1]
                ind = i  # used to be chunkmap[i][0]
        chunkmap.pop(ind)
    return [chunks[c[0]] for c in chunkmap]  # return the chunks as specified in the chunkmap indexes

def main_scheduling(blocks, meetingLength, meetingLockInDate, attendees, minChunks, timeIncrement, meetingName=" "):
    return [{
        "start": r[0], 
        "end": r[1], 
        "can": [attendees[x].user.id for x in r[2]], 
        "cannot": [attendees[x].user.id for x in r[3]]
    } for r in reduce_chunks(blocks, meetingLength, meetingLockInDate, attendees, minChunks, timeIncrement, meetingName)]


### TEST LOADING AND RUNNING

# def testtt_functionnn(i):
#     return i.end.minute - i.start.minute + (i.end.hour - i.start.hour) * 60 + if_neg(i.end.day - i.start.day) * 60 * 24

# print(testtt_functionnn(Block(datetime.datetime(2022, 6, 30, 23, 59), datetime.datetime(2022, 7, 2, 23, 59))))
# print(commitment_check(Commitment(datetime.datetime(2022, 9, 4, 9, 30), datetime.datetime(2022, 9, 4, 9, 45), True), Meeting(" ", datetime.datetime(2022, 9, 4, 9, 15), datetime.datetime(2022, 9, 4, 10, 0), [], datetime.datetime.now())))

# exit()

# with open("backend/scheduling/testdata.json", "r") as read_file:  # loads the test data
#     jsonData = json.load(read_file)

# # print basic information about the test
# print(jsonData["seed"])
# print(jsonData["basetime"])

# # essentially read the json and turn it into classes and datetime objects accordingly
# results = reduce_chunks(
#     blocks = list(map(lambda a: Block(
#         datetime.datetime.fromisoformat(a["start"]), 
#         datetime.datetime.fromisoformat(a["end"])
#         ), jsonData["iBlocks"])),
#     meetingLength = jsonData["iMeetingLength"],
#     meetingLockInDate = jsonData["iMeetingLockInDate"],
#     attendees = list(map(lambda a: MeetingAttendee(
#             User(
#                 a["user"]["name"], 
#                 list(map(lambda b: Commitment(
#                     datetime.datetime.fromisoformat(b["start"]), 
#                     datetime.datetime.fromisoformat(b["end"]), 
#                     b["isAbsolute"]
#                 ), a["user"]["commitments"])),
#                 list(map(lambda b: UserAttendence(
#                     Meeting(
#                         b["meeting"]["name"], 
#                         datetime.datetime.fromisoformat(b["meeting"]["start"]), 
#                         datetime.datetime.fromisoformat(b["meeting"]["end"]),
#                         b["meeting"]["subscribedUsers"],
#                         datetime.datetime.fromisoformat(b["meeting"]["lockInDate"])
#                     ),
#                     b["isCritical"],
#                     b["weight"]
#                 ), a["user"]["meetingSubscriptions"])),
#                 a["user"]["id"]
#             ), 
#             a["isCritical"], 
#             a["weight"]
#         ), jsonData["iAttendees"])),
#     minChunks = jsonData["iMinChunks"],
#     timeIncrement = jsonData["iTimeIncrement"]
# )

# #  processes the results into a json serializable object
# results = list(map(lambda r: {
#     "start": r[0].isoformat(timespec="minutes"), 
#     "end": r[1].isoformat(timespec="minutes"), 
#     "can": list(map(lambda x: jsonData["iAttendees"][x]["user"]["id"], r[2])), 
#     "cannot": list(map(lambda x: jsonData["iAttendees"][x]["user"]["id"], r[3]))
#     }, results))

# #  prints the results and length of the results
# #  print(results)
# print(len(results))

# with open("backend/scheduling/results.json", "w") as write_file:  # downloads the results into another json file
#     json.dump({"seed":jsonData["seed"], "basetime":jsonData["basetime"], "results":results}, write_file, indent=4)