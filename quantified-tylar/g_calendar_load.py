"""
Loads google calendar .ics file and does basic checks.

The .ics file should be exported from gcalendar then placed into the /data
dir.

This script is run from the project root like:

    python .\quantified-tylar\g_calendar_load.py
"""

from datetime import timedelta
import pprint
import re

from icalendar import Calendar

pp = pprint.PrettyPrinter(indent=4)

FNAME = 'data\log_2kmsd7qt9sjc5nqunuglu3utlo@group.calendar.google.com.ics'


event_counts = {}
event_timedeltas = {}

with open(FNAME,'rb') as f_obj:
    gcal = Calendar.from_ical(f_obj.read())
    for component in gcal.walk():
        if component.name != 'VEVENT':
            print('unexpected name :{}'.format(component.name))
        else:
            # VEVENT component keys:
            #   used:
            #       'DTSTART', 'DTEND', SUMMARY
            #
            #  unused:
            #      'LAST-MODIFIED': dt of last modification
            #      'LOCATION':
            #      'SEQUENCE':
            #      'STATUS':
            #      'DTSTAMP' : dt when the event was exported from gcal
            #      'UID':
            #      'CREATED' : dt when the event was CREATED
            #      'DESCRIPTION':
            #      'TRANSP' : transparency (for display?)
            title = str(component.get('summary')).lower()
            event_counts[title] = event_counts.get(title, 0) + 1

            try:
                dt_start = component.get('dtstart').dt
                dt_end = component.get('dtend').dt
                event_len = dt_end - dt_start
                # print(component.get('dtstamp'))
                print(f"{title}\t.\t.\t.\t. += {event_len}")
                event_timedeltas[title] = event_timedeltas.get(title, timedelta(0)) + event_len
            except AttributeError as a_err:
                print(" === event without start/end datetime?")
                print(component.keys())
                print(component.values())
                print(a_err)

print("=== loaded events:")
pp.pprint(event_counts)

# TODO: visualize event counts & timedeltas (bar chart?)
# pp.pprint(event_timedeltas)
