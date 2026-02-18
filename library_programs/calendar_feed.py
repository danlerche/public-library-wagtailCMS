from django.utils import timezone
from datetime import timedelta
from library_programs.models import Event
from open_hours.models import ClosedDate
from wagtail.models import Site
import json

def get_calendar_context(request=None):
    from library_programs.event_base import EventQueries
    eq = EventQueries()
    events_qs = Event.objects.live()
    s_events_qs = Event.objects.filter(repeats__isnull=True).live()
    r_events_qs = Event.objects.filter(repeats__isnull=False).live()
    closed_dates_qs = ClosedDate.objects.select_related("branch_info__closed_holiday_page")
    all_events = eq.all_events(s_events_qs, r_events_qs, closed_dates_qs)

    for event in all_events:
        if event['all_day']:
            event['ics_end_date'] = event['event_date'] + timedelta(days=1)
        else:
            event['ics_end_date'] = event['event_date']

    if request:
        current_site = Site.find_for_request(request)
    else:
        current_site = Site.objects.filter(is_default_site=True).first()

    site_name = current_site.site_name if current_site else "Library Events"

    return {
        'all_events': all_events,
        'site_name': site_name,
    }