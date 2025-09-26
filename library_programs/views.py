#https://docs.wagtail.org/en/stable/extending/admin_views.html#using-base-viewset
from django.db.models import Count
from django.shortcuts import render
from .models import Event, Registration

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
