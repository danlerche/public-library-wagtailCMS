#https://docs.wagtail.org/en/stable/extending/admin_views.html#using-base-viewset
from django.shortcuts import render
from django.db.models import Count
from django.shortcuts import render
from .models import Event, Registration
from .calendar_feed import get_calendar_context
from django.template.loader import render_to_string
from django.http import JsonResponse
import html
from django.utils.html import strip_tags
from datetime import datetime, time, timedelta, timezone as py_timezone # Add 'as py_timezone'

def events_with_registration(request):
    event_qs = Event.objects.filter(enable_registration=True)

    # Registered counts
    num_reg_qs = (
        Registration.objects.filter(wait_list=False)
        .values('event_name_id')
        .annotate(registered=Count('event_name_id'))
    )

    # Waitlist counts
    num_wl_qs = (
        Registration.objects.filter(wait_list=True)
        .values('event_name_id')
        .annotate(wait_listed=Count('event_name_id'))
    )

    # Build lookup dictionaries
    num_reg_lookup = {item['event_name_id']: item['registered'] for item in num_reg_qs}
    num_wl_lookup = {item['event_name_id']: item['wait_listed'] for item in num_wl_qs}

    # Final merged list
    registration_info = [
        {
            'event_name_id': event.id,
            'event_title': event.title,
            'spots_available': event.spots_available,
            'wait_list_spots': event.wait_list_spots,
            'registered': num_reg_lookup.get(event.id, 0),
            'wait_listed': num_wl_lookup.get(event.id, 0),
        }
        for event in event_qs
    ]

    return render(
        request,
        'library_programs/registration/admin_snippet/events_with_registration.html',
        {'registration_info': registration_info},
    )

def event_feed_view(request):
    context = get_calendar_context()
    raw_name = context.get('site_name', 'calendar')
    safe_name = raw_name.lower().replace(" ", "-")
    filename = f"{safe_name}.ics"
    
    #uncomment this section to print the ics feed to the screen 
    # 1. Render the response
    #response = render(
    #    request, 
    #    'library_programs/calendar.ics', 
    #    context, 
    #    # Changed content_type to text/plain to prevent download
    #    content_type='text/plain; charset=utf-8' 
    #)

    # 2. Print the results to your command line
    #print("\n--- BEGIN ICS DEBUG ---")
    #print(response.content.decode('utf-8'))
    #print("--- END ICS DEBUG ---\n")

    #return response

    response = render(
        request, 
        'library_programs/calendar.ics', 
        context, 
        content_type='text/calendar; charset=utf-8'
    )

    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


def event_json_feed(request):
    context = get_calendar_context(request)
    all_events = context.get('all_events', [])

    json_data = []

    for event in all_events:
        start_val = event['ics_start']
        end_val = event['ics_end']
        is_all_day = event.get('all_day', False)

        # ----------------------------------
        # Handle All-Day Events (Excel-safe)
        # ----------------------------------
        if is_all_day:
            # start_val and end_val are dates (or midnight datetimes)
            if isinstance(start_val, datetime):
                start_date = start_val.date()
            else:
                start_date = start_val

            if isinstance(end_val, datetime):
                end_date = end_val.date()
            else:
                end_date = end_val

            # Subtract 1 day because ICS stores all-day end as next day
            end_date = end_date - timedelta(days=1)

            start_out = start_date.strftime('%Y-%m-%d')
            end_out = end_date.strftime('%Y-%m-%d')

        # ----------------------------------
        # Handle Timed Events (Keep UTC)
        # ----------------------------------
        else:
            # Ensure timezone-aware UTC
            if start_val.tzinfo is None or start_val.tzinfo.utcoffset(start_val) is None:
                start_val = start_val.replace(tzinfo=py_timezone.utc)
                end_val = end_val.replace(tzinfo=py_timezone.utc)

            start_out = start_val.isoformat()
            end_out = end_val.isoformat()

        # ----------------------------------
        # Clean Description
        # ----------------------------------
        raw_description = event.get('description', '') or ''
        clean_description = strip_tags(raw_description)
        final_description = html.unescape(clean_description).strip()

        #set sources equal to a closed date equal to 1, and set sources equal to a library event as the value 2. Ensures uniqueness between the two in the JSON id.
        event_type = []
        if event.get('source') == 'closed':
            event_type.append(1)
        elif event.get('source') == 'event':
            event_type.append(2)

        json_data.append({
            "ID": str(event_type[0]) + '-'  + str(event.get('id')) + '-' + str(event.get('occur')),
            "Subject": event.get('title', 'No Title'),
            "Start": start_out,
            "End": end_out,
            "Location": event.get('location', 'Library') or "Library",
            "IsAllDay": is_all_day,
            "Description": final_description
        })

    return JsonResponse(json_data, safe=False)