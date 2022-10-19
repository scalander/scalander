from Meeting_Generation import generate_ics
import datetime
class User:
    def __init__(self,name,emails):
        self.name=name
        self.emails=emails
class UserSubscription:
    def __init__(self, user):
        self.user=user
class MeetingTimeProposal: #test
    def __init__(self,start,end,commitedUsers):
        self.start=start
        self.end=end
        self.commitedUsers=commitedUsers

u1=User("testuser-1","test1@testing.com")
u2=User("testuser-2","test2@testing.com")
u1sub=UserSubscription(u1)
u2sub=UserSubscription(u2)
testmeeting=MeetingTimeProposal(datetime.datetime(2022, 10, 29, 11, 0, 0),datetime.datetime(2022, 10, 29, 12, 30, 0),[u1sub,u2sub])

generate_ics(testmeeting)
#should add a meeting to you google calendar at october 29, 11:00to12:30, with test1@testing.com and test2@testing.com invited
#to do in the future: add more tests/check harder inputs/randomize inputs somehow