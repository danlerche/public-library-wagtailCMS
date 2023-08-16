#date util rrule must be installed for this to work!
#pip install python-dateutil
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django import template
from library_programs.models import Event, EventAge, FullCalendarLink
import datetime, re
import json
from django.db.models import Q

register = template.Library()

def event_base():
    repeating_dates = []
    all_events_orm = Event.objects.live()
    repeating_dates_list = Event.objects.filter(repeats__isnull=False).live()
    single_events_list = Event.objects.filter(repeats__isnull=True).live()
    single_events = []
    repeating_events = []
    full_calendar_link = FullCalendarLink.objects.all()

    for se in single_events_list:
        single_events_dates = datetime.datetime.combine(se.event_date, se.time_to)
        single_event_dict = {'id': se.id, 'event_date':single_events_dates }
        single_events.append(single_event_dict)

    for rd in repeating_dates_list:
    #grabs the repeating dates and formats it from json to a python list
        json_dates_to_list = json.loads(rd.repeating_dates)
        repeating_dates.append(json_dates_to_list)
        for occurrences in range(len(json_dates_to_list)):
            conv_py_dt_format = datetime.datetime.strptime(json_dates_to_list[occurrences], '%Y-%m-%d %H:%M')
            ind_event = {'id': rd.id, 'event_date':conv_py_dt_format }
            repeating_events.append(ind_event)

    all_events = single_events + repeating_events
    #put the event dates in order for a list display of events
    all_events.sort(key=lambda item: item.get('event_date'))
    return all_events, all_events_orm, full_calendar_link

def upcoming_events_base():
    all_events, all_events_orm, full_calendar_link = event_base()
    all_upcoming_events = []
    today = datetime.datetime.now()
    for event_index in range(len(all_events)):
        event_dates = all_events[event_index]['event_date']
        if all_events[event_index]['event_date'] >= today:
            all_upcoming_events.append(all_events[event_index])
    return all_upcoming_events, today

@register.inclusion_tag('library_programs/events_calendar.html', takes_context=True)
def events_calendar(context):
    all_events, all_events_orm, full_calendar_link = event_base()
    return {
        'request': context['request'],
        'all_events': all_events,
        'all_events_orm': all_events_orm,
        }

@register.inclusion_tag('library_programs/all_upcoming_events.html', takes_context=True)
def all_upcoming_events(context):
    all_events, all_events_orm, full_calendar_link = event_base()
    all_upcoming_events, today = upcoming_events_base()

    return {
        'request': context['request'],
        'all_events_orm': all_events_orm,
        'upcoming_events': all_upcoming_events,
        }

@register.inclusion_tag('library_programs/next_three_events_feature.html', takes_context=True)
def next_three_events_feature(context):
    all_events, all_events_orm, full_calendar_link = event_base()
    all_upcoming_events, today = upcoming_events_base()
    hide_from_home_page = []
    hfhp_qs = Event.objects.filter(hide_from_home_page=True)
    #filters out any events the user has asked not to display, using the hide from homepage toggle on the event model
    for ids in hfhp_qs:
        hide_from_home_page.append(ids.id)
    all_upcoming_events = [i for i in all_upcoming_events if not (i['id'] in hide_from_home_page)]
    next_three_events_feature = all_upcoming_events[0:3]
    return {
        'request': context['request'],
        'next_three_events_feature': next_three_events_feature,
        'all_events_orm': all_events_orm,}

@register.inclusion_tag('library_programs/next_four_events_list.html', takes_context=True)
def next_four_events_list(context):
    all_events, all_events_orm, full_calendar_link = event_base()
    all_upcoming_events, today = upcoming_events_base()
    hide_from_home_page = []
    hfhp_qs = Event.objects.filter(hide_from_home_page=True)
    #filters out any events the user has asked not to display, using the hide from homepage toggle on the event model
    for ids in hfhp_qs:
        hide_from_home_page.append(ids.id)
    all_upcoming_events = [i for i in all_upcoming_events if not (i['id'] in hide_from_home_page)]
    next_four_events_list = all_upcoming_events[0:4]
    return {
        'request': context['request'],
        'next_four_events_list': next_four_events_list,
        'all_events_orm': all_events_orm,
        'full_calendar_link': full_calendar_link,}

#Filters upcoming events by a category and sorts it by the next upcoming.
@register.inclusion_tag('library_programs/filtered_upcoming_events_by_cat.html', takes_context=True)
def filtered_upcoming_events_by_cat(context, filter_by):
    today = datetime.datetime.now()
    up_events = Event.objects.live().filter(Q(until__gte=today) | Q(event_date__gte=today, until__isnull=True), event_category__in=filter_by).distinct()
    repeating_dates = []
    next_date = []
    all_upcoming_events = []
    grouped_upcoming_events = []

    for rd in range(len(up_events)):
        if up_events[rd].repeating_dates is not None:
            #grabs the repeating dates in json format and converts them to python dt
            json_dates_to_list = json.loads(up_events[rd].repeating_dates)
            repeating_dates.append(json_dates_to_list)
            for index in range(len(json_dates_to_list)):
                dt_format = datetime.datetime.strptime(json_dates_to_list[index], '%Y-%m-%d %H:%M')
                #grab only the upcoming dates and put each date in their own individual dictionary
                if dt_format >= today:
                    ind_event = {'id': up_events[rd].id, 'repeating_dates':dt_format }
                    all_upcoming_events.append(ind_event)
        #puts the repeating dates in a list grouped by the event id
        rd_list = []
        for aev in all_upcoming_events:
            if aev['id'] == up_events[rd].id and aev['repeating_dates']:
                rd_list.append(aev['repeating_dates'])
        #creates a dictionary with a list of repeating dates if the repeating dates list is not an empty list
        if rd_list != []:
            gr_entry = {'id': up_events[rd].id, 'repeating_dates':rd_list, 'rd': True}
            grouped_upcoming_events.append(gr_entry)
        #filters out single dates and uses the event_date and time_from  db field instead
        elif rd_list == []:
            gr_entry = {'id': up_events[rd].id, 'repeating_dates':datetime.datetime.combine(up_events[rd].event_date, up_events[rd].time_from), 'rd': False}
            grouped_upcoming_events.append(gr_entry)
    #grabs only the next upcoming event.
    for gue in grouped_upcoming_events:
        if gue['rd'] == True:
            next_date.append({'id': gue['id'], 'next_date':gue['repeating_dates'][0]})
        #event_date db field is not a dictionary
        elif gue['rd'] == False:
            next_date.append({'id': gue['id'], 'next_date':gue['repeating_dates']})

    return {
        'request': context['request'],
        'filtered_upcoming_events':up_events,
        'next_date': next_date,
        'today': today,
        }

#Filters upcoming events by a category and sorts it by the audience
@register.inclusion_tag('library_programs/filtered_upcoming_events_by_audience.html', takes_context=True)
def filtered_upcoming_events_by_audience(context, filter_by):
    today = datetime.datetime.now()
    up_events = Event.objects.live().filter(Q(until__gte=today) | Q(event_date__gte=today, until__isnull=True), age_range__audience_name__in=filter_by).distinct()
    repeating_dates = []
    next_date = []
    all_upcoming_events = []
    grouped_upcoming_events = []

    for rd in range(len(up_events)):
        if up_events[rd].repeating_dates is not None:
            #grabs the repeating dates in json format and converts them to python dt
            json_dates_to_list = json.loads(up_events[rd].repeating_dates)
            repeating_dates.append(json_dates_to_list)
            for index in range(len(json_dates_to_list)):
                dt_format = datetime.datetime.strptime(json_dates_to_list[index], '%Y-%m-%d %H:%M')
                #grab only the upcoming dates and put each date in their own individual dictionary
                if dt_format >= today:
                    ind_event = {'id': up_events[rd].id, 'repeating_dates':dt_format }
                    all_upcoming_events.append(ind_event)
        #puts the repeating dates in a list grouped by the event id
        rd_list = []
        for aev in all_upcoming_events:
            if aev['id'] == up_events[rd].id and aev['repeating_dates']:
                rd_list.append(aev['repeating_dates'])
        #creates a dictionary with a list of repeating dates if the repeating dates list is not an empty list
        if rd_list != []:
            gr_entry = {'id': up_events[rd].id, 'repeating_dates':rd_list, 'rd': True}
            grouped_upcoming_events.append(gr_entry)
        #filters out single dates and repeating dates that are less than today
        elif rd_list == []:
            gr_entry = {'id': up_events[rd].id, 'repeating_dates':datetime.datetime.combine(up_events[rd].event_date, up_events[rd].time_from), 'rd': False}
            grouped_upcoming_events.append(gr_entry)
    #grabs only the next upcoming event.
    for gue in grouped_upcoming_events:
        if gue['rd'] == True:
            next_date.append({'id': gue['id'], 'next_date':gue['repeating_dates'][0]})
        #event_date db field is not a dictionary
        elif gue['rd'] == False:
            next_date.append({'id': gue['id'], 'next_date':gue['repeating_dates']})
            
    return {
        'request': context['request'],
        'filtered_upcoming_events':up_events,
        'next_date': next_date,
        'today': today,
        }

#https://github.com/InteractionDesignFoundation/add-event-to-calendar-docs/blob/main/services/google.md
@register.inclusion_tag('library_programs/add_google_calendar.html', takes_context=True)
def add_google_calendar(context, page_id):
    current_event_orm = Event.objects.filter(id=page_id).live()

    all_upcoming_events, today = upcoming_events_base()
    repeating_dates_per_event = []
    for event_index in range(len(all_upcoming_events)):
        is_current_page = page_id in all_upcoming_events[event_index].values()
        if is_current_page == True:
            repeating_dates_per_event.append(all_upcoming_events[event_index])
    return { 
        'repeating_dates_per_event': repeating_dates_per_event,
        'current_event_orm': current_event_orm,
    }

@register.inclusion_tag('library_programs/add_yahoo_calendar.html', takes_context=True)
def add_yahoo_calendar(context, page_id):
    current_event_orm = Event.objects.filter(id=page_id).live()

    #yahoo calendar uses a duration url query string instead of an end date, so we must calculate the difference of start and end date in minutes
    for event_date in current_event_orm:
        time_from = datetime.datetime.combine(event_date.event_date, event_date.time_from)
        time_to = datetime.datetime.combine(event_date.event_date, event_date.time_to)
        dur_td = time_to - time_from
    dur_str = str(dur_td)
    sub = ':'
    repl = '*'
    n = 2
    #convert the time deleta to a string format for the url query by removing seconds, colons and adding a leading zero if necessary
    def format_duration_str(dur_str, sub, repl, n):
        where = [m.start() for m in re.finditer(sub, dur_str)][n-1]
        before = dur_str[:where]
        after = dur_str[where:]
        after = after.replace(sub, repl, 1)
        newString = before + after
        rm_seconds = newString.replace('*00', '')
        to_list = rm_seconds.split(':')
        #yahoo calendar dur url query requires leading zero 
        if len(to_list[0]) == 1:
            duration = '0' + to_list[0] + to_list[1]
        elif len(to_list[0]) == 2:
            duration = to_list[0] + to_list[1]
        return duration
        
    duration = format_duration_str(dur_str, sub, repl, n)

    all_upcoming_events, today = upcoming_events_base()
    repeating_dates_per_event = []
    for event_index in range(len(all_upcoming_events)):
        is_current_page = page_id in all_upcoming_events[event_index].values()
        if is_current_page == True:
            repeating_dates_per_event.append(all_upcoming_events[event_index])
    return { 
        'repeating_dates_per_event': repeating_dates_per_event,
        'current_event_orm': current_event_orm,
        'dur': duration,
        'today': today,
    }
