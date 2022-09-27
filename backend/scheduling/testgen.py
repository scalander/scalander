import json
import os
import datetime
import time
import random
from webbrowser import MacOSX

seed = 1234567890

random.seed(seed)

jsonData = {
    "seed": seed,
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
    start = st  # set start of block
    st += datetime.timedelta(minutes=random.randint(jsonData["iMeetingLength"], 719))  # increment between the start and the end of the block
    jsonData["iBlocks"].append({"start":start.isoformat(timespec="minutes"), "end":st.isoformat(timespec="minutes")})  # set end of block
    st += datetime.timedelta(minutes=random.randint(jsonData["iMeetingLength"], 719))  # increment between end of block and start of next block

def gen_commits(sta, end):  # essentially repeatedly add commitments or free time until it is past the end date
    commitments = []
    ct = sta
    while ct < end:
        if random.choice([True, False]):  # if true add a commitment, if false make it free time
            temp = ct
            ct += datetime.timedelta(minutes=random.randint(1, 90))
            commitments.append({"start":temp, "end":ct})
        else:
            ct += datetime.timedelta(minutes=random.randint(1, 90))
    return commitments

for i in range(random.randint(2, 100)):
    crit = random.choice([True, False])
    weight = random.random() * 10
    user = {"name": f"{random.choice(['John', 'Sara', 'Abigail', 'Charlie', 'Joe', 'Frank', 'José', 'Robert', 'Elizabeth', 'Elijah', 'Theodore'])} {random.choice(['Johnson', 'Andersson', 'Smith', 'Doe', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'])}"}
    user["commitments"] = list(map(lambda c: {"start":c["start"].isoformat(timespec="minutes"), "end":c["end"].isoformat(timespec="minutes"), "isAbsolute":random.choice([True, False])}, gen_commits(stsave, st)))
    user["meetingSubscriptions"] = list(map(lambda m: {"meeting":{"name":" ", "start":m["start"].isoformat(timespec="minutes"), "end":m["end"].isoformat(timespec="minutes"), "subscribedUsers":[], "lockInDate":stsave.isoformat(timespec="minutes")}, "isCritical":random.choice([True, False]), "weight":random.random()*10}, gen_commits(stsave, st)))
    jsonData["iAttendees"].append({"user":user, "isCritical":crit, "weight":weight})






with open("backend/scheduling/testdata.json", "w") as write_file:
    json.dump(jsonData, write_file, indent=4)