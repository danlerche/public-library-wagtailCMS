#https://docs.wagtail.org/en/stable/extending/admin_views.html#using-base-viewset
from django.db.models import Count
from django.shortcuts import render
from .models import Event, Registration

def events_with_registration(request):
	event_qs = Event.objects.filter(enable_registration=True)
	reg_qs = Registration.objects.all()
	num_reg_qs = Registration.objects.filter(wait_list=False).values('event_name_id').annotate(registered=Count('event_name_id'))
	num_wl_qs = Registration.objects.filter(wait_list=True).values('event_name_id').annotate(wait_listed=Count('event_name_id'))
	basic_reg_info = []
	wait_list_info = []

	for ev in event_qs:
		basic_reg_info.append({'event_name_id': ev.id, 'event_title': ev.title, 'spots_available': ev.spots_available, 
			'wait_list_spots': ev.wait_list_spots })

	num_reg_dict = {item['event_name_id']: item for item in num_reg_qs}
	num_wl_dict = {item['event_name_id']: item for item in num_wl_qs}

	if not num_reg_dict:
		registered = 'No Registrations'
	else: 
		registered = num_reg_dict
	
	if not num_reg_dict:
		registration_info = [{'event_name_id': reg_info['event_name_id'], 
		'event_title': reg_info['event_title'], 
		'spots_available': reg_info['spots_available'],
		'wait_list_spots': reg_info['wait_list_spots'],
		'registered': 'No Registrations',
		'wait_listed': next((wl['wait_listed'] 
		for wl in num_wl_qs if wl['event_name_id'] == reg_info['event_name_id']), 0)}  
		for reg_info in basic_reg_info]
	else:
		registration_info = [{'event_name_id': reg_info['event_name_id'], 
		'event_title': reg_info['event_title'], 
		'spots_available': reg_info['spots_available'],
		'wait_list_spots': reg_info['wait_list_spots'],
		'registered': num_reg_dict[reg_info['event_name_id']]['registered'],
		'wait_listed': next((wl['wait_listed'] 
		for wl in num_wl_qs if wl['event_name_id'] == reg_info['event_name_id']), 0)} 
		for reg_info in basic_reg_info]

	return render(request, 'library_programs/registration/admin_snippet/events_with_registration.html', {
        'registration_info': registration_info,
    })

    #'registered': num_reg_dict[reg_info['event_name_id']]['registered'],