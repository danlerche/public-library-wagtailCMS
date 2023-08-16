#currently used to support RSS Feed but may be expanded to cover template tags later
from library_programs.models import Event
from library_programs.feeds import UpcomingEventsFeed
import datetime, re, json
from django.db.models import Q
from library_programs.feeds import UpcomingEventsFeed

class EventBase():
    today = datetime.datetime.now()
    thirty_days = today + datetime.timedelta(30)
    repeating_dates = []
    repeating_events = []
    single_events = []
    repeating_dates_list = Event.objects.filter(repeats__isnull=False).live()
    single_events_list = Event.objects.filter(repeats__isnull=True).live()
    all_upcoming_events = []
    next_month_events = []
    
    for se in single_events_list:
        link = se.url
        single_events_dates = datetime.datetime.combine(se.event_date, se.time_to)
        single_event_dict = {'id': se.id, 'title': se.title, 'event_date':single_events_dates, 'description':se.description, 'url':link }
        single_events.append(single_event_dict)

    for rd in repeating_dates_list:
        link = rd.url
    #grabs the repeating dates and formats it from json to a python list
        json_dates_to_list = json.loads(rd.repeating_dates)
        repeating_dates.append(json_dates_to_list)
        for occurrences in range(len(json_dates_to_list)):
            conv_py_dt_format = datetime.datetime.strptime(json_dates_to_list[occurrences], '%Y-%m-%d %H:%M')
            ind_event = {'id': rd.id, 'title': rd.title, 'event_date':conv_py_dt_format, 'description': rd.description, 'url':link }
            repeating_events.append(ind_event)

    all_events = single_events + repeating_events
    #put the event dates in order for a list display of events
    all_events.sort(key=lambda item: item.get('event_date'))

    for event_index in range(len(all_events)):
        event_dates = all_events[event_index]['event_date']
        if all_events[event_index]['event_date'] >= today and all_events[event_index]['event_date'] <= thirty_days:
            next_month_events.append(all_events[event_index])
    
