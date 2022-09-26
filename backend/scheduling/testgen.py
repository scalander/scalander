import json
import os
import datetime
import time
import random

seed = 1234567890

random.seed(seed)

jsonData = {
    "iBlocks": [],
    "iMeetingLength": random.randint(10, 90),
    "iMeetingLockInDate": datetime.datetime.now().isoformat(),
    "iAttendees": [],
    "iMinChunks": random.randint(3, 10),
    "iTimeIncrement": random.randint(1, 10)
}
td = 0
for i in range(random.randint(1, 10)):
    start = datetime.datetime.now()  # a lot of stuff to do, remember to remove seconds and milliseconds

with open("backend/scheduling/testdata.json", "w") as write_file:
    json.dump(jsonData, write_file, indent=4)