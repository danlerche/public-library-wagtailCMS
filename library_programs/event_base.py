import datetime, re
import json
from django.http import JsonResponse

#this class has a number of reusable functions to display data in template tags and the RSS feed. 

class EventQueries:
    #creates a list of dictionaries that contain both events with repeating dates and one-off events in event date order
    def all_events(self, s_events_qs, r_events_qs):
        single_events = []
        #formats single events into a list of dictionaries so they can be combined with repeating dates
        for se in s_events_qs:
            se_dates = datetime.datetime.combine(se.event_date, se.time_from)
            se_dict = {'id': se.id, 'title':se.title, 'event_date':se_dates, 'description':se.description, 'url':se.url }
            single_events.append(se_dict)
        
        repeating_dates = []
        repeating_events = []
        #repeating dates are stored as an individual json field inside the event model. Json dates are converted to python dates. 
        #For every repeating date a new dictionary is created. Thereby one event with multiple dates will display as multiple seperate events. 
        for rd in r_events_qs:
            json_dates_to_list = json.loads(rd.repeating_dates)
            repeating_dates.append(json_dates_to_list)
            for occur in range(len(json_dates_to_list)):
                py_dt_format = datetime.datetime.strptime(json_dates_to_list[occur], '%Y-%m-%d %H:%M')
                ind_event = {'id': rd.id, 'title':se.title, 'event_date':py_dt_format, 'description':se.description, 'url':se.url }
                repeating_events.append(ind_event)
        all_events = single_events + repeating_events
        all_events.sort(key=lambda item: item.get('event_date'))
        return all_events

    def all_upcoming_events(self, all_events):
        all_upcoming_events = []
        today = datetime.datetime.now()
        for event_index in range(len(all_events)):
            event_dates = all_events[event_index]['event_date']
            if all_events[event_index]['event_date'] >= today:
                all_upcoming_events.append(all_events[event_index])
                all_upcoming_events
        return all_upcoming_events

    #displays single and recurring events with the next date of the recurrence showing
    def next_upcoming_events(self, upcoming_event_qs):
        all_upcoming_events = []
        today = datetime.datetime.now()
        repeating_dates = []
        grouped_upcoming_events = []
        next_date = []
        repeating_dates = []
        next_date = []
        all_upcoming_events = []
        grouped_upcoming_events = []

        for rd in range(len(upcoming_event_qs)):
            if upcoming_event_qs[rd].repeating_dates is not None:
                #grabs the repeating dates in json format and converts them to python dt
                json_dates_to_list = json.loads(upcoming_event_qs[rd].repeating_dates)
                repeating_dates.append(json_dates_to_list)
                for index in range(len(json_dates_to_list)):
                    dt_format = datetime.datetime.strptime(json_dates_to_list[index], '%Y-%m-%d %H:%M')
                    #grab only the upcoming dates and put each date in their own individual dictionary
                    if dt_format >= today:
                        ind_event = {'id': upcoming_event_qs[rd].id, 'repeating_dates':dt_format }
                        all_upcoming_events.append(ind_event)
            #puts the repeating dates in a list grouped by the event id
            rd_list = []
            for aev in all_upcoming_events:
                if aev['id'] == upcoming_event_qs[rd].id and aev['repeating_dates']:
                    rd_list.append(aev['repeating_dates'])
            #creates a dictionary with a list of repeating dates if the repeating dates list is not an empty list
            if rd_list != []:
                gr_entry = {'id': upcoming_event_qs[rd].id, 'repeating_dates':rd_list, 'rd': True, 'time_from':upcoming_event_qs[rd].time_from, 'time_to':upcoming_event_qs[rd].time_to,'title':upcoming_event_qs[rd].title, 'event_image':upcoming_event_qs[rd].event_image , 'url':upcoming_event_qs[rd].url }
                grouped_upcoming_events.append(gr_entry)
            #filters out single dates and uses the event_date and time_from  db field instead
            elif rd_list == []:
                gr_entry = {'id': upcoming_event_qs[rd].id, 'repeating_dates':datetime.datetime.combine(upcoming_event_qs[rd].event_date, upcoming_event_qs[rd].time_from), 'rd': False, 'time_from':upcoming_event_qs[rd].time_from, 'time_to':upcoming_event_qs[rd].time_to,'title':upcoming_event_qs[rd].title, 'event_image':upcoming_event_qs[rd].event_image , 'url':upcoming_event_qs[rd].url}
                grouped_upcoming_events.append(gr_entry)
        #grabs only the next upcoming event.
        for gue in grouped_upcoming_events:
            if gue['rd'] == True:
                next_date.append({'id': gue['id'],'next_date':gue['repeating_dates'][0],'time_from': gue['time_from'], 'time_to': gue['time_to'],'title': gue['title'],'event_image': gue['event_image'] ,'url': gue['url']})
            #event_date db field is not a dictionary
            elif gue['rd'] == False:
                next_date.append({'id': gue['id'],'next_date':gue['repeating_dates'], 'time_from': gue['time_from'], 'time_to': gue['time_to'],'title': gue['title'],'event_image': gue['event_image'] ,'url': gue['url']})
        return next_date