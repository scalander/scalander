#IMPORTS
from fcntl import F_SEAL_SEAL
import time
from operator import truediv

#FUNCTIONS
def commitmentCheck(commitment, meeting): #if meeting and commitment intersect, return True
    return ((meeting.start>commitment.start and meeting.start<commitment.end) or (meeting.end>commitment.start and meeting.end<commitment.end))

def checkUserCommits(meeting, user): #check all the user's commitments with a meeting, return True if meeting time works
    for c in user.commitments:
        if commitmentCheck(c, meeting):
            return False
    return True

def checkUserSubs(meeting, user): #check all the user's meeting subscriptions with a meeting, return True if meeting time works
    for c in user.meetingSubscriptions:
        if commitmentCheck(c.meeting, meeting):
            return False
    return True

def checkBoth(meeting, user): #check both subs and commits, return True if it still works
    return (checkUserCommits(meeting, user) and checkUserSubs(meeting, user))
