#for getting the freebusy status from the user
#TODO: figure out how to test this
from calendar_api.calendar_api import google_calendar_api
import json
g = google_calendar_api()
calendar = g.list() #gets the list of calendars that the user is subscribed to as an object
cal_ids = [] #for storing the "id" field of all the users calendars
formatted_ids = [] #for storing the calendar IDs in the format that query() takes
query_max = "2022-10-30T00:00:00Z" #latest date-time to check for freebusy - currently a placeholder but will eventually be user input (as specified by RFC3339 https://www.rfc-editor.org/rfc/rfc3339#section-5.6)
query_min = "2022-9-1T00:00:00Z" #eariliest date-time to check - see query_max

for cal in calendar.items: #appends all calendar IDs to cal_id
    cal_ids.append(cal.id)

for id in cal_ids: #adds calendar IDs to formatted_ids in the format needed in query body
    formatted_ids.append({
        "id": id
    })

g.query(body = {
    "calendarExpansionMax": 50, # Maximal number of calendars for which FreeBusy information is to be provided. Optional. Maximum value is 50.
    "groupExpansionMax": 100, # Maximal number of calendar identifiers to be provided for a single group. Optional. An error is returned for a group with more members than this value. Maximum value is 100.
    "timeMax": query_max, # The end of the interval for the query formatted as per RFC3339.
    "items": formatted_ids,
    "timeMin": query_min, # The start of the interval for the query formatted as per RFC3339.
    "timeZone": "UTC", # Time zone used in the response. Optional. The default is UTC.
#structure for query body from: https://google-api-client-libraries.appspot.com/documentation/calendar/v3/python/latest/calendar_v3.freebusy.html
})

