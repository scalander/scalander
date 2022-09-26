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
    "iMeetingLockInDate": datetime.datetime.now().isoformat(timespec="minutes"),
    "iAttendees": [],
    "iMinChunks": random.randint(3, 10),
    "iTimeIncrement": random.randint(1, 10)
}
st = datetime.datetime.now() + datetime.timedelta(days=random.randint(0,30), hours=random.randint(0,23), minutes=random.randint(0,59))
stsave = st
for i in range(random.randint(1, 15)):
    start = st
    st += datetime.timedelta(minutes=random.randint(jsonData["iMeetingLength"], 719))
    jsonData["iBlocks"].append({"start":start, "end":st})
    st += datetime.timedelta(minutes=random.randint(jsonData["iMeetingLength"], 719))

def gen_commits(sta, end):
    commitments = []
    
    return commitments

for i in range(random.randint(2, 100)):
    crit = random.choose([True, False])
    weight = random.random()
    user = {"name": f"{random.choose(['John', 'Sara', 'Abigail', 'Charlie', 'Joe', 'Frank', 'José', 'Robert', 'Elizabeth', 'Elijah', 'Theodore'])} {random.choose(['Johnson', 'Hughes', 'Smith', 'Doe', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'])}"}







with open("backend/scheduling/testdata.json", "w") as write_file:
    json.dump(jsonData, write_file, indent=4)