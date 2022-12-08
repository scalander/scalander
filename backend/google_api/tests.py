from django.test import TestCase

# import datetime
import datetime

# import code to test
from google_api import get_freebusy

# import faker
from faker import Faker

# import mock http calls
from googleapiclient.discovery import build
from googleapiclient.http import HttpMock
from google.oauth2.credentials import Credentials

#try out pprint
import pprint

#tests all of the google calendar api things
class GcalTestCase(TestCase):

    def setUp(self):
        self.cases = [{
            "start": datetime.datetime(2020, 10, 10, 3, 2, 4),
            "end": datetime.datetime(2020, 12, 10, 3, 2, 4) 
        },{
            "start": "2022-10-10",
            "end": "2022-12-10"
        }] #TODO: test string start datetime end
        self.tzoffset = "-08:00" #TODO: when timezones work, fix these tests

        #mock api calls:
        calhttp = HttpMock("google_api/mock_calendar_response.py")
        freebusyhttp = HttpMock("mock_freebusy_response.py")
        service = build("calendar", http=calhttp , credentials=Credentials())
        self.calendar_response = service.calendarList().list().execute()
        self.freebusy_response = service.freebusy().query().execute()
        service.close
        self.request = 0 #TODO: make request
        self.send_request = 0

    def tearDown(self):
        del self.cases
    
    def test_make_query(self):
        for case in self.cases:
            body = get_freebusy.make_query(case["start"], case["end"])
            if type(case["start"]) == datetime.date or type(case["start"]) == datetime.datetime:
                self.assertTrue(body["timeMin"] == case["start"].strftime()+ "T00:00:00" +self.tzoffset, "query min does not match input")
            elif type(case["start"]) == str:
                self.assertTrue(body["timeMin"] == case["start"] + "T00:00:00" +self.tzoffset)

            if type(case["end"]) == datetime.date or type(case["end"]) == datetime.datetime:
                self.assertTrue(body["timeMax"] == case["end"].strftime() + "T00:00:00" +self.tzoffset, "query max does not match input")
            elif type(case["end"]) == str:
                self.assertTrue(body["timeMax"] == case["end"] + "T00:00:00" +self.tzoffset)
    
    def test_format_all(self):
        cals = get_freebusy.format_all(self.response)

        self.assertTrue(type(cals) == list)
        self.assertTrue(cals != []) #TODO: use this to check if its the expected output once i have one

    def test_link_names(self):
        names = get_freebusy.link_names(self.response)

        #TODO: assert resopnse matches

    def test_send_commitments(self):
        self.send_request
            


    