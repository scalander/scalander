import datetime
#date format is year+month+day+T+hour+minute+i think second+Z (everything has leading zeroes if one digit)
base_event='''BEGIN:VEVENT
DTSTART:20220912T130000Z
DTEND:20220912T140000Z
DTSTAMP:20220911T235846Z
UID:2gkvfd12bimc4euolu2h7491dp@google.com
CREATED:20220911T235754Z
DESCRIPTION:
LAST-MODIFIED:20220911T235754Z
LOCATION:
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:Test Item
TRANSP:OPAQUE
END:VEVENT'''

x = datetime.datetime(2022, 9, 11, 14, 0, 0)

def datetime_to_ics(time):
    time2=[str(time.month),str(time.day),str(time.hour),str(time.minute),str(time.second)]
    for i in range(len(time2)):
        if len(time2[i]) == 1:
            time2[i] = "0"+time2[i]
    newtime=str(time.year)+time2[0]+time2[1]+"T"+time2[2]+time2[3]+time2[4]+"Z"
    return newtime
#takes in json for meeting and ics file
def AddMeeting(meeting,ics_name):
    ics = open(ics_name, "r+")
    ics_lines = ics.readlines()
    add_line = ics_lines[-2]





#AddMeeting(meeting,template)

print(datetime_to_ics(x))