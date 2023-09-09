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

#make the queryset it's own function so we don't have to keep writing them!

def db_queries():
    today = datetime.datetime.now()
    events_qs = Event.objects.live()
    s_events_qs = Event.objects.filter(repeats__isnull=True).live()
    r_events_qs = Event.objects.filter(repeats__isnull=False).live()
    featured_event = Event.objects.live().filter(Q(until__gte=today, until__isnull=False, featured_on_home_page=True) | \
        Q(event_date__gte=today, until__isnull=True, featured_on_home_page=True))
    full_calendar_link = FullCalendarLink.objects.all()
    return today, events_qs, s_events_qs, r_events_qs, featured_event, full_calendar_link

@register.inclusion_tag('library_programs/events_calendar.html', takes_context=True)
def events_calendar(context):
    today, events_qs, s_events_qs, r_events_qs, featured_event, full_calendar_link = db_queries()
    from library_programs.event_base import EventQueries
    eq = EventQueries()
    all_events = eq.all_events(s_events_qs, r_events_qs)

    return {
        'request': context['request'],
        'all_events': all_events,
        'events_qs': events_qs,
        }

@register.inclusion_tag('library_programs/all_upcoming_events.html', takes_context=True)
def all_upcoming_events(context):
    today, events_qs, s_events_qs, r_events_qs, featured_event, full_calendar_link = db_queries()
    from library_programs.event_base import EventQueries
    eq = EventQueries()
    all_events = eq.all_events(s_events_qs, r_events_qs)
    upcoming_events = eq.all_upcoming_events(all_events)

    return {
        'request': context['request'],
        'events_qs': events_qs,
        'upcoming_events': upcoming_events,
        }

@register.inclusion_tag('library_programs/next_four_events_list.html', takes_context=True)
def next_four_events_list(context):
    today, events_qs, s_events_qs, r_events_qs, featured_event, full_calendar_link = db_queries()
    from library_programs.event_base import EventQueries
    eq = EventQueries()
    all_events = eq.all_events(s_events_qs, r_events_qs)
    upcoming_events = eq.all_upcoming_events(all_events)
    next_four_events_list = upcoming_events[0:4]

    return {
        'request': context['request'],
        'next_four_events_list': next_four_events_list,
        'events_qs': events_qs,
        'full_calendar_link': full_calendar_link,}

@register.inclusion_tag('library_programs/next_three_events_feature.html', takes_context=True)
def next_three_events_feature(context):
    today, events_qs, s_events_qs, r_events_qs, featured_event, full_calendar_link = db_queries()
    from library_programs.event_base import EventQueries
    eq = EventQueries()
    next_events = eq.next_upcoming_events(featured_event)
    next_three_events = sorted(next_events, key=lambda x: x['next_date'])[:3]

    return {
    'request': context['request'],
    'next_three_events':next_three_events,
    'featured_event': featured_event, 
    }

#Filters upcoming events by a category and sorts it by the next upcoming.
@register.inclusion_tag('library_programs/filtered_upcoming_events_by_category.html', takes_context=True)
def filtered_upcoming_events_by_cat(context, filter_by):
    today = datetime.datetime.now()
    events_by_cat = Event.objects.live().filter(Q(until__gte=today) | Q(event_date__gte=today, until__isnull=True), event_category__in=filter_by).distinct()
    from library_programs.event_base import EventQueries
    eq = EventQueries()
    next_date = eq.next_upcoming_events(events_by_cat)
    
    return {
        'request': context['request'],
        'filtered_upcoming_events':events_by_cat,
        'next_date': next_date,
        'today': today,
        }

#Filters upcoming events by audience and sorts it by the next upcoming.
@register.inclusion_tag('library_programs/filtered_upcoming_events_by_audience.html', takes_context=True)
def filtered_upcoming_events_by_audience(context, filter_by):
    today = datetime.datetime.now()
    events_by_aud = Event.objects.live().filter(Q(until__gte=today) | Q(event_date__gte=today, until__isnull=True), age_range__audience_name__in=filter_by).distinct()
    from library_programs.event_base import EventQueries
    eq = EventQueries()
    next_date = eq.next_upcoming_events(events_by_aud)
    
    return {
        'request': context['request'],
        'filtered_upcoming_events':events_by_aud,
        'next_date': next_date,
        'today': today,
        }

#https://github.com/InteractionDesignFoundation/add-event-to-calendar-docs/blob/main/services/google.md
@register.inclusion_tag('library_programs/add_google_calendar.html', takes_context=True)
def add_google_calendar(context, page_id):
    current_event_qs = Event.objects.filter(id=page_id).live()
    today, events_qs, s_events_qs, r_events_qs, featured_event, full_calendar_link = db_queries()
    from library_programs.event_base import EventQueries
    eq = EventQueries()
    all_events = eq.all_events(s_events_qs, r_events_qs)
    upcoming_events = eq.all_upcoming_events(all_events)

    repeating_dates_per_event = []
    for event_index in range(len(upcoming_events)):
        is_current_page = page_id in upcoming_events[event_index].values()
        if is_current_page == True:
            repeating_dates_per_event.append(upcoming_events[event_index])
    return { 
        'repeating_dates_per_event': repeating_dates_per_event,
        'current_event_qs': current_event_qs,
    }

@register.inclusion_tag('library_programs/add_yahoo_calendar.html', takes_context=True)
def add_yahoo_calendar(context, page_id):
    current_event_qs = Event.objects.filter(id=page_id).live()
    today, events_qs, s_events_qs, r_events_qs, featured_event, full_calendar_link = db_queries()
    from library_programs.event_base import EventQueries
    eq = EventQueries()
    all_events = eq.all_events(s_events_qs, r_events_qs)
    upcoming_events = eq.all_upcoming_events(all_events)

    #yahoo calendar uses a duration url query string instead of an end date, so we must calculate the difference of start and end date in minutes
    for event_date in current_event_qs:
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

    repeating_dates_per_event = []
    for event_index in range(len(upcoming_events)):
        is_current_page = page_id in upcoming_events[event_index].values()
        if is_current_page == True:
            repeating_dates_per_event.append(upcoming_events[event_index])
    return { 
        'repeating_dates_per_event': repeating_dates_per_event,
        'current_event_qs': current_event_qs,
        'dur': duration,
        'today': today,
    }
