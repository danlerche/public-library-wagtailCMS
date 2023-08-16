# To do
# create conditions for multiday, single day, open hours and closing soon to return true or false
from django import template
from datetime import timedelta
from open_hours.models import EnableMessageDisplay, OpenHour, ClosedDate, BranchInfo
import datetime as dt
from django.db.models import Q

register = template.Library()

@register.inclusion_tag('open_hours/hours.html', takes_context=True)
def open_hours(context):
	request = context['request']
	branch_info = BranchInfo.objects.all()
	current_date = dt.date.today()
	current_time = dt.datetime.now().time()
	week_day = dt.date.today().weekday()
	closed_date_from = ClosedDate.objects.values('closed_date_from')
	closed_date_to = ClosedDate.objects.values('closed_date_to')
	closed_holiday = ClosedDate.objects.filter(closed_date_from=current_date, all_day=True)
	multiday_holiday = ''
	multiday_alt_hour = ''
	close_time = ""
	minutes_remaining = ""
	seconds_remaining = ""
	close_times_list = OpenHour.objects.filter(day_of_the_week=week_day, open_closed=1).values('time_to')

	#checks to see if there's a closed date that has beginning before or equal to today and an end date greater or equal to today
	is_multiday =  ClosedDate.objects.filter(closed_date_from__lte=current_date, closed_date_to__gte=current_date).values('closed_date_from', 'closed_date_to')
	#if the list is empty, do nothing
	if not is_multiday:
		cdf = ''
		cdt = ''
	else:
		#gets the dictory values for closed and open dates
		cdf = is_multiday[0].get('closed_date_from')
		cdt = is_multiday[0].get('closed_date_to')
		# checks if the raw from and to dates are the same. If they are, it's not a multiday
		if cdf == cdt:
			multiday_holiday = ''
			close_times_list = ClosedDate.objects.filter(closed_date_from=current_date, all_day=False).values('time_to')
		else:
			multiday_holiday = ClosedDate.objects.filter(closed_date_from__lte=current_date, closed_date_to__gte=current_date, all_day=True)
			multiday_alt_hour = ClosedDate.objects.filter(closed_date_from__lte=current_date, closed_date_to__gte=current_date, all_day=False)
			close_times_list = ClosedDate.objects.filter(closed_date_from__lte=current_date, all_day=False).values('time_to')
	alt_hour = ClosedDate.objects.filter(closed_date_from=current_date,all_day=False)
	open_hour = OpenHour.objects.filter(day_of_the_week=week_day, open_closed=1)
	# use this to display closed message during an opening day, when not during opening hours
	#open_hour = OpenHour.objects.filter(day_of_the_week=week_day, open_closed=1, time_from__lte=current_time, time_to__gte=current_time)
	next_holiday = ClosedDate.objects.filter(closed_date_from__gt=current_date,all_day=True).order_by('closed_date_from')[:1]
	enable_message_display = EnableMessageDisplay.objects.all()

#prevents no list error
	if not close_times_list:
		subtract = ""
		minutes_remaining = ""
		close_time = ""
		seconds_remaining = ""
	else:
		close_times_dict = close_times_list[0]
		close_time = close_times_dict.get('time_to')
		boiler_plate_year = dt.date(1, 1, 1)
		current_time_combine = dt.datetime.combine(boiler_plate_year, current_time)
		time_to_combine = dt.datetime.combine(boiler_plate_year, close_time)
		subtract = time_to_combine - current_time_combine
		if subtract < dt.timedelta(minutes=60) and subtract > dt.timedelta(minutes=0):
			minutes_remaining = str(subtract).split(':')[1]
			seconds_remaining = str(subtract).split(':')[2].split('.')[0]

			#might want to add seconds to this
		#elif subtract < dt.timedelta(minutes=0):
		#	minutes_remaining = 'closed'

	return {'request':	request,
			'branch_info': branch_info,
			'open_hour': open_hour,
			'closed_date_from': closed_date_from,
			'closed_date_to': closed_date_to,
			'week_day':	week_day,
			'current_date': current_date,
			'current_time': current_time,
			'multiday_holiday': multiday_holiday,
			'closed_holiday': closed_holiday,
			'alt_hour': alt_hour,
			'multiday_alt_hour': multiday_alt_hour,
			'next_holiday': next_holiday,
			'enable_message_display': enable_message_display,
			'close_time': close_time,
			'subtract': subtract,
			'minutes_remaining': minutes_remaining,
			'seconds_remaining': seconds_remaining
			}

@register.inclusion_tag('open_hours/business_hours.html', takes_context=True)
def business_hours(context):
	request = context['request']
	business_hour = OpenHour.objects.all().order_by('day_of_the_week')

	return {'request':	request,
			'business_hour': business_hour}

@register.inclusion_tag('open_hours/next_closure.html', takes_context=True)
def next_closure(context):
	request = context['request']
	branch_info = BranchInfo.objects.all()
	current_date = dt.date.today()
	next_closure = ClosedDate.objects.filter(closed_date_from__gt=current_date,all_day=True).order_by('closed_date_from')[:1]

	return {'request':	request,
			'next_closure': next_closure,
			'branch_info': branch_info}

@register.inclusion_tag('open_hours/all_closures.html', takes_context=True)
def all_closures(context):
	request = context['request']
	current_date = dt.date.today()
	all_closures = ClosedDate.objects.filter(closed_date_from__lte=current_date, closed_date_to__gte=current_date).order_by('closed_date_from') | ClosedDate.objects.filter(closed_date_from__gt=current_date).order_by('closed_date_from')
	#all_closures = ClosedDate.objects.filter(closed_date_from__gt=current_date,all_day=True).order_by('closed_date_from')
	#alt_hours = ClosedDate.objects.filter(closed_date_from__gt=current_date,all_day=False).order_by('closed_date_from')

	return {'request':	request,
			'today': current_date,
			'all_closures': all_closures,
			#'alt_hours':alt_hours
			}
