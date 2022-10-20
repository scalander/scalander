import time
import datetime  # necessary
import json  # necessary
import random
import os
from scheduling import *


with open("backend/scheduling/testdata.json", "r") as read_file:  # loads the test data
    jsonData = json.load(read_file)

# print basic information about the test
# print(jsonData["seed"])
# print(jsonData["basetime"])

# essentially read the json and turn it into classes and datetime objects accordingly
results = reduce_chunks(
    blocks = list(map(lambda a: Block(
        datetime.datetime.fromisoformat(a["start"]), 
        datetime.datetime.fromisoformat(a["end"])
        ), jsonData["iBlocks"])),
    meetingLength = jsonData["iMeetingLength"],
    meetingLockInDate = jsonData["iMeetingLockInDate"],
    attendees = list(map(lambda a: MeetingAttendee(
            User(
                a["user"]["name"], 
                list(map(lambda b: Commitment(
                    datetime.datetime.fromisoformat(b["start"]), 
                    datetime.datetime.fromisoformat(b["end"]), 
                    b["isAbsolute"]
                ), a["user"]["commitments"])),
                list(map(lambda b: UserAttendence(
                    Meeting(
                        b["meeting"]["name"], 
                        datetime.datetime.fromisoformat(b["meeting"]["start"]), 
                        datetime.datetime.fromisoformat(b["meeting"]["end"]),
                        b["meeting"]["subscribedUsers"],
                        datetime.datetime.fromisoformat(b["meeting"]["lockInDate"])
                    ),
                    b["isCritical"],
                    b["weight"]
                ), a["user"]["meetingSubscriptions"])),
                a["user"]["id"]
            ), 
            a["isCritical"], 
            a["weight"]
        ), jsonData["iAttendees"])),
    minChunks = jsonData["iMinChunks"],
    timeIncrement = jsonData["iTimeIncrement"]
)

#  processes the results into a json serializable object
results = list(map(lambda r: {
    "start": r[0].isoformat(timespec="minutes"), 
    "end": r[1].isoformat(timespec="minutes"), 
    "can": list(map(lambda x: jsonData["iAttendees"][x]["user"]["id"], r[2])), 
    "cannot": list(map(lambda x: jsonData["iAttendees"][x]["user"]["id"], r[3]))
    }, results))

#  prints the results and length of the results
#  print(results)
# print(len(results))

with open("backend/scheduling/results.json", "w") as write_file:  # downloads the results into another json file
    json.dump({"seed":jsonData["seed"], "basetime":jsonData["basetime"], "results":results}, write_file, indent=4)
