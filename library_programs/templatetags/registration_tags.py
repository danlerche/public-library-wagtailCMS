from django import template
from django.shortcuts import render
from library_programs.models import Registration

register = template.Library()

@register.inclusion_tag('library_programs/registration/submission_parse.html', takes_context=True)

def show_registrations(context, filter_by):
	all_registrations = Registration.objects.all()
	user_info = Registration.objects.user_info.form_data
	
	return {
        'request': context['request'],
        'all_registrations': all_registrations,
        }
