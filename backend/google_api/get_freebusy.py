#for getting the freebusy status from the user
#TODO: figure out how to test this
from calendar_api.calendar_api import google_calendar_api
import json
import datetime
today = datetime.today.strftime("%Y-%m-%d")
g = google_calendar_api()
calendar = g.list() #gets the list of calendars that the user is subscribed to as a dictionary
cal_ids = [] #for storing the "id" field of all the users calendars
formatted_ids = [] #for storing the calendar IDs in the format that query() takes
query_max = today #latest date-time to check for freebusy - default is midnight 1 week from today (as specified by RFC3339 https://www.rfc-editor.org/rfc/rfc3339#section-5.6)
query_min = today + datetime.timedelta(days = 7) #eariliest date-time to check - default is midnight today, see query_max TODO: make this 1 week from today
commitments = []


def format_all(cals = calendar): #takes in a list of the user's calendars - default is all
    #takes in a set of the user's calendars from the google api and formats and returns them to be used in a freebusy query - use get_freebusy()
    for cal in cals.items: #appends all calendar IDs to cal_id
        cal_ids.append(cal["id"])

    for id in cal_ids: #adds calendar IDs to formatted_ids in the format needed in query body
        formatted_ids.append({
            "id": id
        })
    return(formatted_ids)


def get_freebusy(formatted_ids = formatted_ids, query_max = query_max, query_min = query_min):
    freebusy = g.query(body = {
        "calendarExpansionMax": 50, # Maximal number of calendars for which FreeBusy information is to be provided. Optional. Maximum value is 50.
        "groupExpansionMax": 100, # Maximal number of calendar identifiers to be provided for a single group. Optional. An error is returned for a group with more members than this value. Maximum value is 100.
        "timeMax": query_max, # The end of the interval for the query formatted as per RFC3339. default is 1 week from today
        "items": formatted_ids, #IDs of the user's calendars - use format_all() to get these
        "timeMin": query_min, # The start of the interval for the query formatted as per RFC3339. default is today
        "timeZone": "UTC", # Time zone used in the response. Optional. The default is UTC.
    #structure for query body from: https://google-api-client-libraries.appspot.com/documentation/calendar/v3/python/latest/calendar_v3.freebusy.html
    })
    # return (freebusy["busy"])
    send_commitments(freebusy["busy"])

def send_commitments(freebusy): #runs from get_freebusy() - you shouldn't need to run this
    for commitment in freebusy:
        start = datetime.datetime.strptime(commitment["start"], "%Y-%m-%dT%H:%M:%S%z") #start of a commitment turned into a datetime object
        end = datetime.datetime.strptime(commitment["end"], "%Y-%m-%dT%H:%M:%S%z") #end of a commitment turned into a datetime object
        commitments.append({
            "start": start,
            "end": end,
            "isAbsolute": True #can't really be sure from freebusy so we assume true
        })
    return(commitments)

