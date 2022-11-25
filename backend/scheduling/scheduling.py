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

def block_in_blocks(block:Block, blocks:List[Block]):
    """utility function to check if a block is in blocks

    Arguments:
        block: Block - block to check if its in...
        blocks: [Block] - these blocks

    Returns:
        bool - is `block` in `blocks`?
    """

    for b in blocks:
        # starts after start and ends before end means its in
        if block.start >= b.start and block.end <= b.end:
            return True

    return False
    

def sweep(commitments):
    """the sweep line algorithm

    USACO style :sunglasses:

    Arguments:
        commitments: [(UID_TYPE, (datetime, datetime))] - the list of commitments to sweep

    Returns:
        a list [([UID_TYPE... ], Block)...] representing possible chunks
       and when they are available

    Implementation:
        This is implemented as the classic sweep-line with some greedyness mixed in. We
        will go through the commitments, split into "push" and "pop" actions on a stack
        then sort them. We then set an epoch (line) through the times.
        As our list is now guaranteed sorted, we know our NEXT element
        will start at least after if not with our current element (it is monotonic). Hence,
        we will keep intervals that intersect by sweeping through and keeping thrack of
        who's available.

        m = time blocks, n = availbilities
        Sweep O(m), Sort O(nlogn), Total: O(max(nlogn,m))

        See: http://www.usaco.org/index.php?page=viewproblem2&cpid=786
    """

    # if we have no commitments from nobody, do nothing
    if len(commitments) == 0:
        return []

    # we begin by splitting our commitments into two events
    # START event, and END event. This allow us to sweep a line
    # through the events.
    flattened = [] # each is ("START/END", ticket_id, time)
    for c in commitments:
        flattened.append(("START", c[0], c[1][0]))
        flattened.append(("END", c[0], c[1][1]))

    # now, our next job is to sort it so thaht flattened is
    # monotonic.
    # sort commitments by their start date
    flattened = sorted(flattened, key=lambda x:x[2])


    # generated scratch blocks (should contain Block objects)
    blocks = []
    # generated availabilities (should contain tuples of IDs)
    availabilities = []

    # pop the top to seed our search
    c1 = flattened.pop(0)

    # CONFUSING: c1 is the FIRST commitment object
    # online is an arary of who's "online" (i.e. on the line being sweeped),
    # "epoch" is where the line currently is (at the start of the first commitment) 
    #
    # if confused see solution to lifegards problem linked above
    # the first block is also garanteed to be START
    online = [c1[1]]
    epoch = c1[2]

    # until we have read all
    while len(flattened) > 0:
        # get the next one
        c = flattened.pop(0)

        # terminate and push the last block
        # which started at the last epoch (where line was)
        # and ends at this new start
        new_block = Block(epoch, c[2])
        # we push this and the old online info to what we have
        # this is given that we had somebody online during this
        # block (i.e. its possible the block ended but the next
        # one didn't start yet)
        if len(online) > 0:
            blocks.append(new_block)
            availabilities.append(online.copy())

        # if we have a START event
        if c[0] == "START":
            # now, our new patron is available, so we push
            # them on the list
            online.append(c[1])
        # if we have an END event
        elif c[0] == "END":
            # now, our new patron is unavailable, so we remove
            # them from the list
            online.remove(c[1])

        # we set our epoch to when the last modification happened
        epoch = c[2]


    return list(zip(availabilities, blocks))

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

    # get a list of user's commitments
    # note that commitments here mean times for which the user *is* available
    # map from ticket:commitment

    commitments = [] # each object (ticket_id, (start,end))

    for ticket in tickets:
        # get uid
        uid = api.get_uid_by_subscription(ticket)
        # check commitments and append
        user_commitments = api.get_commitments_by_user(uid)
        # we will create a list of ticket, commitment
        commitments += [(ticket, (c.start, c.end)) for c in user_commitments]
        
    # now we have chunks and people's availability in them,
    # we will parcel them out 
    chunks = sweep(commitments)
    # recall each object: [([UID_TYPE... ], Block)...]

    # final proposals
    proposals = []

    # for each time block, we then create **one** chunk
    # This is important. Now, if we just made all the chunks, the user would have
    # about 5 different proposals which is literally just 5 minutes apart --- if
    # they have a large block shared. This is no bueno.
    #
    # Therefore, we only make one time proposal per chunk
    for chunk in chunks:
        # check if proposed block is long enough
        meeting_fits = (chunk[1].end-chunk[1].start).seconds//60 > meeting_length

        if meeting_fits and block_in_blocks(chunk[1], schedule_during):
            # create the start and end time
            start = chunk[1].start
            end = start+datetime.timedelta(minutes=meeting_length)
            # tickets that can make it is in the first item
            can = chunk[0]
            # cannot is those tickets that are not in can
            cannot = list(filter(lambda x:x not in can, tickets))
            # calculate weight 
            total_weight = sum(api.get_attendance(i).weight for i in can)

            # create the proposal
            proposals.append(Proposal(start, end, can, cannot, total_weight))
           
    # return all meaningful blocks
    return proposals
                                
def schedule(ranges:List[Block], meeting_length: int, tickets: int,
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

