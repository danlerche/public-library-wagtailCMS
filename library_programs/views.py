#https://docs.wagtail.org/en/stable/extending/admin_views.html#using-base-viewset
from django.shortcuts import render
from django.db.models import Count
from django.shortcuts import render
from .models import Event, Registration
from .calendar_feed import get_calendar_context
#delete this line below later
from django.template.loader import render_to_string

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