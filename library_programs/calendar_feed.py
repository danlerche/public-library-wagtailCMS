from django.utils import timezone
from datetime import datetime, time, timedelta, timezone as py_timezone
from library_programs.models import Event
from open_hours.models import ClosedDate
from wagtail.models import Site

def get_calendar_context(request=None):
    from library_programs.event_base import EventQueries
    eq = EventQueries()
    
    # Fetching your various querysets
    events_qs = Event.objects.live()
    s_events_qs = Event.objects.filter(repeats__isnull=True).live()
    r_events_qs = Event.objects.filter(repeats__isnull=False).live()
    closed_dates_qs = ClosedDate.objects.select_related("branch_info__closed_holiday_page")
    
    # Getting the combined list of dictionaries
    all_events = eq.all_events(s_events_qs, r_events_qs, closed_dates_qs)

    for event in all_events:
        if event['all_day']:
            # All-day events: Date only, no UTC conversion needed
            event['ics_start'] = event['event_date']
            # Outlook fix: End date must be the next day
            event['ics_end'] = event['event_date'] + timedelta(days=1)
        else:
            # Timed events: Combine date and time
            # Note: event['event_date'] might be a datetime, so we call .date()
            start_dt = datetime.combine(event['event_date'].date(), event['time_from'])
            end_dt = datetime.combine(event['event_date'].date(), event['time_to'])
            
            # Make the datetime "Aware" (uses America/Vancouver from settings.py)
            if timezone.is_naive(start_dt):
                start_dt = timezone.make_aware(start_dt)
                print(start_dt)
                end_dt = timezone.make_aware(end_dt)

            # Convert to UTC for the ICS Z-suffix
            event['ics_start'] = start_dt.astimezone(py_timezone.utc)
            event['ics_end'] = end_dt.astimezone(py_timezone.utc)

    # Site lookup logic
    if request:
        current_site = Site.find_for_request(request)
    else:
        current_site = Site.objects.filter(is_default_site=True).first()

    site_name = current_site.site_name if current_site else "Library Events"

    return {
        'all_events': all_events,
        'site_name': site_name,
        'now': timezone.now(),
    }