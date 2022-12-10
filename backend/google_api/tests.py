from django.test import TestCase

# import datetime
import datetime

# import code to test
from google_api import get_freebusy

#import expected value
from google_api import mock_output

# import mock http calls
from googleapiclient.discovery import build
from googleapiclient.http import HttpMock

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
        calhttp = HttpMock("google_api/mock_calendar_response.json")
        freebusyhttp = HttpMock("google_api/mock_freebusy_response.json")
        service = build("calendar", "v3", http=calhttp)
        self.calendar_response = service.calendarList().list().execute()
        service.close
        service = build("calendar", "v3", http=freebusyhttp)
        self.freebusy_response = service.freebusy().query().execute()
        service.close

    def tearDown(self):
        del self.cases
    
    def test_make_query(self):
        for case in self.cases:
            body = get_freebusy.make_query(case["start"], case["end"])
            if type(case["start"]) == datetime.date or type(case["start"]) == datetime.datetime:
                self.assertTrue(body["timeMin"] == case["start"].strftime("%Y-%m-%d")+ "T00:00:00" +self.tzoffset, "query min does not match input")
            elif type(case["start"]) == str:
                self.assertTrue(body["timeMin"] == case["start"] + "T00:00:00" +self.tzoffset)

            if type(case["end"]) == datetime.date or type(case["end"]) == datetime.datetime:
                self.assertTrue(body["timeMax"] == case["end"].strftime("%Y-%m-%d") + "T00:00:00" +self.tzoffset, "query max does not match input")
            elif type(case["end"]) == str:
                self.assertTrue(body["timeMax"] == case["end"] + "T00:00:00" +self.tzoffset)
    
    def test_format_all(self):
        cals = get_freebusy.format_all(self.calendar_response)
        self.assertEqual(cals,[{'id': 'n1bis749a5nh1oiid6cjkf2d407lgojq@import.calendar.google.com'}, {'id': 'jonwu@nuevaschool.org'}, {'id': '85h7n2emq6p062lcvq13qbt41to18hk9@import.calendar.google.com'}], "format_all() response incorrect")

    def test_link_names(self):
        self.names = get_freebusy.link_names(self.calendar_response)
        self.assertEqual(self.names, {'n1bis749a5nh1oiid6cjkf2d407lgojq@import.calendar.google.com': 'Jonathan Wu Calendar (Canvas)', 'jonwu@nuevaschool.org': 'main', '85h7n2emq6p062lcvq13qbt41to18hk9@import.calendar.google.com': 'Nueva Calendar'}, "link_names() response incorrect")

    def test_send_commitments(self):
        names = get_freebusy.link_names(self.calendar_response)
        result = get_freebusy.send_commitments(self.freebusy_response,names)
        self.assertEqual(result,mock_output.data)
            


    