import datetime
import json
import api_app.api as api

class Block:
    def __init__(self, start, end):
        self.start, self.end = start, end

# functions here generally call the one(s) directly above them

def commitment_check(commitment_id, time):  # if time and commitment intersect, return True
    commitment = api.get_commitment(commitment_id)
    return (commitment.start <= time.start) and (commitment.end >= time.end)

def check_user_commits(time, user):  # check all the user's commitments with a meeting, return True if meeting time works
    for c in api.get_user(user).commitments:
        if commitment_check(c, time):
            return True
    return False  # add isAbsolute functionality to commitments later

def check_multiple_users(time, users):
    can, cannot = [], []
    for u in users:
        if check_user_commits(time, u):
            can.append(u)
        else:
            cannot.append(u)
    return [can, cannot]

def check_all_times(times, users):  # times is a list of the meeting object (not rly storage efficient but whatever)
    return list(map(lambda t: check_multiple_users(t, users), times))

def chunk_times(times, users):
    # TODO note that while times are Meeting() objects, they are hijacked
    # to have .start and .end to be the start and end PROPOSAL times
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

# reduce_chunks used to be above create times but it caused chunks to not be reduced correctly

def if_neg(n):  # return 1 if the number is negative (basically if it crosses months I have to return one because it crosses days, else return the normal so it does whatever it normally would do)
    if n < 0:
        return 1
    else:
        return n

def create_times(blocks, meetingLength, meetingLockInDate, attendees, minChunks, timeIncrement, meetingName):  # timeIncrement is the increment between start times in minutes (>1), meetingLength is the length of the meeting in minutes (>1), meetingName is unnecessary
    # this is all under the assumption of <12h blocks, but will still work as long as they are under 24 hours
    chunks = []
    for i in blocks:
        times = []
        # meetingLength must be less than blockLen
        blockLen = i.end.minute - i.start.minute + (i.end.hour - i.start.hour) * 60 + if_neg(i.end.day - i.start.day) * 60 * 24
        # if meetingLength > blockLen: return -1  # figure out a way to throw errors later
        timeQuantity = (blockLen - meetingLength) // timeIncrement + 1
        for j in range(timeQuantity):  # go through the block and add a time every time increment
            # TODO refactor. this is API abuse but we are creating "meeting" objects
            times.append(api.Meeting(meetingName, i.start + datetime.timedelta(minutes=timeIncrement*j), i.start + datetime.timedelta(minutes=meetingLength+timeIncrement*j), 30, [], attendees, meetingLockInDate))  # change Meeting class later once we standardize the classes
        chunks += chunk_times(times, list(map(lambda a: api.get_attendee(a).user, attendees)))
    return chunks

def reduce_chunks(blocks, meetingLength, meetingLockInDate, attendees, minChunks, timeIncrement, meetingName=" "):
    chunks, chunkmap = create_times(blocks, meetingLength, meetingLockInDate, attendees, minChunks, timeIncrement, meetingName), []  # attendees is a list of the MeetingAttendee model, user is a child
    for i in range(len(chunks)):  # chunkmap format is as such: [[chunkIndex, value], ...]
        shouldContinue = False
        for ii,j in enumerate(chunks[i][3]):
            # TODO: optimize by caching
            attendee = api.get_attendee(attendees[ii])
            if attendee.is_critical:
                shouldContinue = True
                break
        if shouldContinue:
            continue
        value = 0
        for ii,j in enumerate(chunks[i][2]):
            # JANK: essentially somewhere we didn't clarify
            # that "ATTENDEE" is a meeting request ticket.
            #
            # therefore, we need to reconsiliate the fact
            # that CHUNKS is returning Users but we need
            # UserMeetingSubscription IDs. However, their ORDER
            # should match. THerefore, we are just getting the
            # nth order by user.
            attendee = api.get_attendee(attendees[ii])
            if not attendee.is_critical:
                value += attendee.weight
        chunkmap.append([i, value])
    while len(chunkmap) > minChunks:  # chunkmap could potentially return less than minChunks values, which is fine
        # should maybe add a loop count limit to prevent crash abuse once I figure out errors
        indvalue, ind = chunkmap[0][1], 0
        for i in range(1, len(chunkmap)):
            if chunkmap[i][1] < indvalue:
                indvalue = chunkmap[i][1]
                ind = i  # used to be chunkmap[i][0]
        chunkmap.pop(ind)
    return list(map(lambda c: chunks[c[0]], chunkmap))  # return the chunks as specified in the chunkmap indexes

def schedule(blocks, meetingLength, meetingLockInDate, attendees, minChunks, timeIncrement, meetingName=" "):
    result = reduce_chunks(blocks, meetingLength, meetingLockInDate, attendees, minChunks, timeIncrement, meetingName)
    return list(map(lambda chunk: {
        "start": chunk[0], 
        "end": chunk[1], 
        "can": chunk[2], 
        "cannot": chunk[3]
    }, result))


### TEST LOADING AND RUNNING

def test_main():
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
        attendees = list(map(lambda a: api.MeetingAttendee(
                api.User(
                    a["user"]["name"], 
                    list(map(lambda b: api.Commitment(
                        datetime.datetime.fromisoformat(b["start"]), 
                        datetime.datetime.fromisoformat(b["end"]), 
                        b["isAbsolute"]
                    ), a["user"]["commitments"])),
                    list(map(lambda b: api.UserAttendence(
                        api.Meeting(
                            b["meeting"]["name"], 
                            datetime.datetime.fromisoformat(b["meeting"]["start"]), 
                            datetime.datetime.fromisoformat(b["meeting"]["end"]),
                            30,
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
    print(len(results))

    with open("backend/scheduling/results.json", "w") as write_file:  # downloads the results into another json file
        json.dump({"seed":jsonData["seed"], "basetime":jsonData["basetime"], "results":results}, write_file, indent=4)
