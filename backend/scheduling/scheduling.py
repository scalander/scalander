import datetime
import json
import api_app.api as api
import time as ttt # because time is a variable name
import datetime

from typing import List

# data classes
from dataclasses import dataclass

@dataclass
class Block:
    """A Block of Time (duration) start+end
    @dataclass

    Members:
       start: datetime.datetime - start time of block
       end: datetime.datetime - end time of block
    """
    start: datetime.datetime
    end: datetime.datetime

@dataclass
class Proposal:
    """A proposal for time availability
    @dataclass

    Members:
       start: datetime.datetime - start time of block
       end: datetime.datetime - end time of block
       can: [int] - tickets that can make it
       cannot: [int] - tickets that cannot make it
       total_weight: int - total weights of those can make it
    """

    start: datetime.datetime
    end: datetime.datetime
    can: List[int]
    cannot: List[int]
    total_weight: int

# functions here generally call the one(s) directly above them

def check_multiple_users(time: Block, tickets: List[int]) -> dict:
    """Checks whether a list of tickets is available at a specific time

    Arguments:
        time: Block - a time block to check
        tickets: [int] - a list of meeting tickets
                         (UserMeetingSubscription IDs) to check

    Returns:
        {"can": [int - available tickets],
         "cannot": [int - unavailable tickets]}
    """

    # build mappings between UID and subscription ticket ID
    # (to read the output of checking)
    uid_to_ticket = {api.get_uid_by_subscription(i):i for i in tickets}

    # check for users that can make it (we pass uid)
    result = api.check_commitment(list(uid_to_ticket.keys()), time.start, time.end)
    # map back to tickets
    can = [uid_to_ticket[i] for i in result]

    # those that cannot make it are the rest
    cannot = list(filter(lambda x:x not in can, tickets))

    return {"can": can, "cannot": cannot}

def check_all_times(times: [Block], tickets: List[int]) -> List[Proposal]:
    """Returns whether or not a list of users is available for a list

    Arguments:
        times: [Block] - a list of blocks to check
        tickets: [int] - a list of tickets
                         (UserMeetingSubscription IDs) to check

    Returns:
        a list of Proposals
    """

    # we will calculate the users' availabilities
    availabilities = [check_multiple_users(t, tickets) for t in times]
    # tallyed proposals
    proposals = []

    # we will deserialize the blocks onto each availiblity
    # to create proposals
    for time, avail in zip(times, availabilities):
        avail["start"] = time.start
        avail["end"] = time.end

        # now, we need to tally the weights of those tha
        # can make it and get their total weight
        weight = 0
        
        # for each ticket, add
        for ticket_id in avail["can"]:
            info = api.get_attendance(ticket_id)
            weight += info.weight

        # set it back to avail object
        avail["total_weight"] = weight

        proposals.append(Proposal(**avail))
    
    return proposals

def create_time_chunks(ranges:[Block], meeting_length:int,
                       time_increment:int) -> List[Block]:
    """Creates a list of `Blocks` of `timeIncrement` length between `ranges`

    Arguments:
        ranges: [Block] - ranges of times in which to create smaller chunks of 
        meeting_length: int - number of **minutes** which the meeting should last
        time_increment: int - number of **minutes** that should be between the starts
                              of two blocks of output (how close should proposals be?)

    Returns:
        list of `Blocks` for possible chunks
    """

    chunks = []
    
    # our meeting length, as a timedelta
    meeting_length_delta = datetime.timedelta(minutes=meeting_length)
    time_increment_delta = datetime.timedelta(minutes=time_increment)

    # for each range
    for r in ranges:
        # get the start time, and start iterating by time_increment
        # epoch is our pointer of start of blocks
        epoch = r.start

        # for as long as we didn't hit the ending yet
        # recall `epoch` is the poniter to start so
        # we subtract a meeting_length_delta
        while epoch < r.end-meeting_length_delta:
            # append the chunk, as it works
            chunks.append(Block(epoch, epoch+meeting_length_delta))
                
            # check the next time increment 
            epoch += time_increment_delta

    # return the generated chunks
    return chunks
    

def create_times(schedule_during:[Block], meeting_length,
                 tickets, time_increment=5) -> List[Proposal]:
    """creates suitable times and calculates user availability


    Arguments:
        ranges: [Block] - ranges of times in which to create smaller chunks of 
        meeting_length: int - number of **minutes** which the meeting should last
        tickets: int - the UserMeetingSubscription ticket IDs for the participating users
        [time_increment]: int - number of **minutes** that should be between the starts
                                of two blocks of output (how close should proposals be?)

    Returns:
        a list of Proposals representing the meaningful times we have created
    """

    # create the possible chunks
    chunks = create_time_chunks(schedule_during, meeting_length, time_increment)

    # check the times and create proposals
    proposals = check_all_times(chunks, tickets)

    # abort if we have nothing
    if len(proposals) == 0:
        return []

    # This is important. Now, if we just returned the result, the user would have
    # about 5 different proposals which is literally just 5 minutes apart --- if
    # they have a large block shared. This is no bueno.
    #
    # Therefore, we iterate through the times and remove "redundant" chunks --- keeping
    # only the top one. What does "redundant" mean? Two chunks are redundant IFF they
    # have the 1) same availability (can, cannot) and 2) are `time_increment` minutes
    # apart only.

    # create an array of meaningful blocks, starting with the first proposal
    meaningful_proposals = [proposals.pop(0)]

    # recall thath we are comparing agaist last time, not just last menangful
    # time, to do meaningful blocks (i.e. otherwise we will schedule over
    # things like long contiousl blocks where every *n* will be meannigful)
    last = proposals.pop(0)

    # for each proposal, check if its meaningful against the last
    # this assumes that the times are sorted. which they should be if
    # generated
    for proposal in proposals:
        # check for attendee
        if (proposal.can != last.can) or (proposal.cannot != last.cannot):
            meaningful_proposals.append(proposal)
            last = proposal # set comp
            continue

        # check for time delta, if its larger than time_increment, then its meaningufl
        # timedelta doesn't store minutes arg
        if (proposal.start-last.start).seconds//60 > time_increment:
            meaningful_proposals.append(proposal)
            last = proposal # set comp
            continue

        # otherwise, they are not meaningful so we don't append
        last = proposal # set comp

    # return all meaningful blocks
    return meaningful_proposals
                                
def schedule(ranges:[Block], meeting_length: int, tickets: int,
             time_increment=5, max_chunks:int=None) -> List[Proposal]:
    """Performs scheduling `meeting_length` blocks for `tickets` between `ranges` 

    Arguments:
        ranges: [Block] - ranges of times in which to create smaller chunks of 
        meeting_length: int - number of **minutes** which the meeting should last
        tickets: int - the UserMeetingSubscription ticket IDs for the participating users
        [time_increment]: int - number of **minutes** that should be between the starts
                                of two blocks of output (how close should proposals be?)
        [max_chunks]: int - the maximum number of chunks to return

    Returns:
        a list of Proposals representing the meaningful times we have created,
        sortedy by weight
    """

    # get scratch results
    result = create_times(ranges, meeting_length, tickets, time_increment)

    # sort the results by weight
    result = list(reversed(sorted(result, key=lambda x:x.total_weight)))

    # crop and return result
    # note that cropping by None does nothing, so this behavior is acceptable
    return result[:max_chunks]

