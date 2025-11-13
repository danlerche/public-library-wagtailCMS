from django.db import models
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel, PageChooserPanel, TabbedInterface, ObjectList
from wagtail.fields import RichTextField
from wagtail.admin.forms import WagtailAdminPageForm
import datetime, json, pytz
from datetime import time, timedelta
from django import forms
from dateutil.rrule import *
from dateutil.parser import *
from django.utils.html import strip_tags
from django.http import HttpResponse
from icalendar import Calendar, Event, Alarm, vDate
from icalendar import Event as icsEvent, vDatetime, vText
#registration imports
from wagtail.contrib.forms.models import AbstractFormField, AbstractForm, AbstractEmailForm, AbstractFormSubmission
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
from wagtail.snippets.views.snippets import DeleteView
from wagtail_honeypot.models import (
    HoneypotFormMixin, HoneypotFormSubmissionMixin
)
from django.utils.html import format_html, format_html_join

class EventAudience(ClusterableModel):
    audience_name = models.CharField(max_length=300, null=True, blank=True)

    panels = [
    FieldPanel('audience_name'),
    ]

    def __str__(self):
        return self.audience_name

class EventAge(ClusterableModel):
    age_range = models.CharField(max_length=300, null=True, blank=True)
    audience_name = models.ForeignKey(EventAudience, on_delete=models.SET_NULL, null=True, blank=True)


    panels = [
    FieldPanel('age_range'),
    FieldPanel('audience_name'),
    ]


    def __str__(self):
        return self.age_range

class EventCategory(ClusterableModel):
    category_name = models.CharField(max_length=300, null=True, blank=True)

    panels = [
    FieldPanel('category_name'),
    ]

    def __str__(self):
        return self.category_name

WEEKDAY_CHOICE = (
    ("Sunday", "Sunday"),
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
)

WEEK_INTERVAL_CHOICE = (
    (1, "The First"),
    (2, "The Second"),
    (3, "The Third"),
    (4, "The Fourth"),
    (-1, "The Last"),
)

REPEAT_CHOICE = (
    ("DAILY", "Daily"),
    ("WEEKLY", "Weekly"),
    ("MONTHLY", "Monthly"),
    ("YEARLY", "Yearly"),
    ("CUSTOM", "Custom"),
)

class FullCalendarLinkForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()
        link_to_calendar = cleaned_data['link_to_calendar']
        already_exists = FullCalendarLink.objects.count()
        if already_exists > 0:
            self.add_error('link_to_calendar', "You may only have one link to a full calendar")
        return cleaned_data

class FullCalendarLink(models.Model):
    link_to_calendar = models.ForeignKey('wagtailcore.Page', null=True, blank=False, on_delete=models.CASCADE, related_name='+',)
    base_form_class = FullCalendarLinkForm
    def __str__(self):
        return self.link_to_calendar.title

class EventEditExtraValidation(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()
        # make sure that if repeats is selected that the user has also entered something in the until field
        repeats = cleaned_data['repeats']
        until = cleaned_data['until']
        week_interval = cleaned_data['week_interval']
        weekday = cleaned_data['weekday']
        enable_registration = cleaned_data['enable_registration']
        registration_form_chooser = cleaned_data['registration_form_chooser']
        success_page = cleaned_data['success_page']
        if repeats is not None and until is None:
            self.add_error('until', 'please enter an until date or deselect the repeats option')
        elif repeats == 'CUSTOM' and week_interval is None:
            self.add_error('week_interval', 'Week interval cannot be blank if Custom is selected')
        elif repeats == 'CUSTOM' and weekday is None:
            self.add_error('weekday', 'Weekday cannot be blank if Custom is selected')
        if enable_registration == 1 and registration_form_chooser is None:
            self.add_error('registration_form_chooser', 'Registration form must be chosen to enable registration')
        if enable_registration == 1 and success_page is None:
            self.add_error('success_page', 'Success page must be chosen to enable registration')

    def save(self, commit=True):
        page = super().save(commit=False)
        #sets the time from midnight to 11:59pm if all day is checked in the admin
        if page.all_day:
            page.time_from = time(0, 0)      # 00:00
            page.time_to = time(23, 59)      # 23:59
        #repeat rule logic starts here
        #needed for the if statement to evaluate to True or False
        event_repeats = str(page.repeats)
        week_interval = page.week_interval
        weekday = page.weekday
        if weekday == 'Sunday':
            weekday_intial = 'SU'
        elif weekday == 'Monday':
            weekday_intial = 'MO'
        elif weekday == 'Tuesday':
            weekday_intial = 'TU'
        elif weekday == 'Wednesday':
            weekday_intial = 'WE'
        elif weekday == 'Thursday':
            weekday_intial = 'TH'
        elif weekday == 'Friday':
            weekday_intial = 'FR'
        elif weekday == 'Saturday':
            weekday_intial = 'SA'
        else: weekday_intial = weekday

        if week_interval is not None and weekday is not None:
            byweekday_value = weekday_intial + '(' + str(week_interval) + ')'
        else:
            byweekday_value = ''

        #use the rrule module to generate repeating dates
        repeating_dates = []

        event_start = datetime.datetime.combine(page.event_date, page.time_from)
        if page.until is not None:
             #creates a custom repeat rule string to be inclued with the rrule value such as every 3rd Thursday, etc
             #need to add 1 day to the date until value in order for the final date to be included in the repeating dates field
            custom_monthly_rrl_str = "FREQ=MONTHLY;" + "BYWEEKDAY=" + byweekday_value + ';UNTIL=' + str(page.until + datetime.timedelta(days=1))
            event_end = datetime.datetime.combine(page.until, page.time_from)

            exception_dates =  []
            #querying the ParentalKey of the event model, where the exception_dates is the related_name of the model
            ed_qs = [ed.exception_date for ed in page.exception_dates.all()]
            for ed_index in range(len(ed_qs)):
                exception_dates.append(datetime.datetime.combine(ed_qs[ed_index], page.time_from))
            if event_repeats == 'DAILY' and not exception_dates:
                rrule_rd = list(rrule(freq=DAILY, until=event_end, dtstart=event_start))
            elif event_repeats == 'DAILY' and exception_dates:
                rrule_rd = list(rrule(freq=DAILY, until=event_end, dtstart=event_start))
                rrule_rd = [ed for ed in rrule_rd if ed not in exception_dates]

            elif event_repeats == 'WEEKLY' and not exception_dates:
                rrule_rd = list(rrule(freq=WEEKLY, until=event_end, dtstart=event_start))
            elif event_repeats == 'WEEKLY' and exception_dates:
                rrule_rd = list(rrule(freq=WEEKLY, until=event_end, dtstart=event_start))
                rrule_rd = [ed for ed in rrule_rd if ed not in exception_dates]

            elif event_repeats == 'MONTHLY' and not exception_dates:
                rrule_rd = list(rrule(freq=MONTHLY, until=event_end, dtstart=event_start))

            elif event_repeats == 'MONTHLY' and exception_dates:
                rrule_rd = list(rrule(freq=MONTHLY, until=event_end, dtstart=event_start))
                rrule_rd = [ed for ed in rrule_rd if ed not in exception_dates]

            elif event_repeats == 'YEARLY' and not exception_dates:
                rrule_rd = list(rrule(freq=YEARLY, until=event_end, dtstart=event_start))
            elif event_repeats == 'YEARLY' and exception_dates:
                rrule_rd = list(rrule(freq=YEARLY, until=event_end, dtstart=event_start))
                rrule_rd = [ed for ed in rrule_rd if ed not in exception_dates]

            elif event_repeats == 'CUSTOM' and not exception_dates:
                rrule_rd = list(rrulestr(custom_monthly_rrl_str, dtstart=event_start))
            elif event_repeats == 'CUSTOM' and exception_dates:
                rrule_rd = list(rrulestr(custom_monthly_rrl_str, dtstart=event_start))
                rrule_rd = [ed for ed in rrule_rd if ed not in exception_dates]

            else:
                rrule_rd = []

            #If the user changes an event from custom, back to another repeat type, clears all the weekday and week interval db values
            if event_repeats != 'CUSTOM' and week_interval is not None:
                page.week_interval = None
            if event_repeats != 'CUSTOM' and weekday is not None:
                page.weekday = None

            for rrule_index in range(len(rrule_rd)):
                format_date = rrule_rd[rrule_index].strftime("%Y-%m-%d %H:%M")
                repeating_dates.append(format_date)
                #converts to JSON style year month day format and appends to the master list
            #converts repeating dates to JSON format and CRUD (updates) the repeating dates field in the datebase
            page.repeating_dates = json.dumps(repeating_dates)

        #if a page changes from a repeating type to null, delete the repeating dates and weekday
        if page.repeats is None and page.repeating_dates is not None:
            page.repeating_dates = None
            page.weekday = None
            page.week_interval = None

        if commit:
            page.save()
        return page

class Event(Page, Orderable):
    event_category = ParentalKey(EventCategory, on_delete=models.SET_NULL, related_name='event_category', null=True, blank=True)
    age_range = ParentalManyToManyField("EventAge", blank=True)
    event_date = models.DateField(null=True,blank=True)
    time_from = models.TimeField(null=True, blank=True)
    time_to = models.TimeField(null=True, blank=True)
    all_day = models.BooleanField(default=False, help_text="Check if this event is all day")
    description = RichTextField(max_length=1500,null=True,blank=True)
    repeats = models.CharField(max_length = 20, choices = REPEAT_CHOICE, null=True, blank=True)
    until = models.DateField(null=True,blank=True)
    week_interval = models.IntegerField(choices = WEEK_INTERVAL_CHOICE, null=True, blank=True)
    weekday = models.CharField(max_length = 20, choices = WEEKDAY_CHOICE, null=True, blank=True)
    event_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL,related_name='+')
    featured_on_home_page = models.BooleanField(default=True)
    repeating_dates = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True, help_text="Enter a location where the event will happen")
    form_page = models.ForeignKey('wagtailcore.Page', blank=True, null=True, on_delete=models.SET_NULL, related_name='embedded_form_page', help_text='Select a Form that will be embedded on this page.')
    tutorial_link = models.CharField(max_length=255, blank=True, help_text="for showing Niche Academy Links or similar")
    #fields used to registrer for a library program
    enable_registration = models.BooleanField(default=False)
    spots_available = models.PositiveIntegerField(default=0)
    wait_list_spots = models.PositiveIntegerField(default=0,)
    registration_form_chooser = models.ForeignKey('wagtailcore.Page', blank=True, null=True, on_delete=models.SET_NULL, related_name='embedded_registration_form_page', help_text='Select a Registration Form that will be embedded on this page.')
    enable_email = models.BooleanField(default=False)
    success_email_msg = RichTextField(blank=True, null=True, verbose_name="Body of the success email")
    waitlist_email_msg = models.CharField(max_length=2000, blank=True, null=True, verbose_name="Body of the waitlist email")
    success_page = models.ForeignKey('wagtailcore.Page', blank=True, on_delete=models.SET_NULL, null=True, related_name="registration_success")
    close_reg_date = models.DateTimeField(null=True, blank=True, verbose_name="Close Registration Form", help_text="Date the registration form will be removed from the page. Otherwise closes after the program ends.")

    def clean(self):
        super().clean()
        # If not all-day, require both time_from and time_to
        if not self.all_day:
            if not self.time_from:
                raise ValidationError({'time_from': "This field is required if 'All day' is not checked."})
            if not self.time_to:
                raise ValidationError({'time_to': "This field is required if 'All day' is not checked."})

            # Ensure time_from < time_to
            if self.time_from and self.time_to and self.time_from >= self.time_to:
                raise ValidationError({'time_to': "End time must be after start time."})

        if self.close_reg_date is not None:
            if self.close_reg_date.date() > self.event_date:
                raise ValidationError({"Close Registration Form Field cannot be later than the event date."})

    def show_registered_events():
        return self.Event.objects.get(enable_registration=1)

    def serve(self, request, form_submission=None, *args, **kwargs):
        registered = Registration.objects.filter(event_name_id=self.page_ptr_id, wait_list=0).count()
        wait_listed = Registration.objects.filter(event_name_id=self.page_ptr_id, wait_list=1).count()
        reg_spots_remaining = self.spots_available - registered
        wait_list_remaining = self.wait_list_spots - wait_listed
        event_id = Event.objects.get(id=self.page_ptr_id)
      
        event_date_time_to = datetime.datetime.combine(self.event_date, self.time_to)
        if self.until is not None: 
            until_date_time_to = datetime.datetime.combine(self.until, self.time_to)
        else:
            until_date_time_to = ''
        #function to generate .ics files for integration into calendars
        def create_ical(title, desc, start, end, until, curr_date, repeats, ics_week_interval, ics_weekday, time_from, exdate, location, all_day, event_date):
            cal = Calendar()
            cal.add('prodid', '-//Events at the Penticton Public Library//NONSGML v1.0//EN')
            cal.add('version', '2.0')
            alarm = Alarm()
            alarm['action'] = 'DISPLAY'
            alarm['description'] = "Reminder"
            alarm['trigger'] = '-PT60M'  # 60 minutes before the event
            ics_event = icsEvent()
            ics_event.add('summary', title)
            ics_event.add('description', desc)
            ics_event.add_component(alarm)
            if all_day:
                dtstart = vDate(event_date)
                dtend = vDate(event_date)
            else:    
                dtstart = vDatetime(start)
                dtend = vDatetime(end)
            dtstart.params['TZID'] = 'PACIFIC STANDARD TIME'
            dtend.params['TZID'] = 'PACIFIC STANDARD TIME'
            ics_event.add('dtstart', dtstart)
            ics_event.add('dtend', dtend)
            if repeats == 'CUSTOM' and ics_weekday is not None:
                if ics_weekday == 'Sunday':
                    ics_week_interval = str(ics_week_interval) + 'SU'
                elif ics_weekday == 'Monday':
                    ics_week_interval = str(ics_week_interval) + 'MO'
                elif ics_weekday == 'Tuesday':
                    ics_week_interval = str(ics_week_interval) + 'TU'
                elif ics_weekday == 'Wednesday':
                    ics_week_interval = str(ics_week_interval) + 'WE'
                elif ics_weekday == 'Thursday':
                    ics_week_interval = str(ics_week_interval) + 'TH'
                elif ics_weekday == 'Friday':
                    ics_week_interval = str(ics_week_interval) + 'FR'
                elif ics_weekday == 'Saturday':
                    ics_week_interval = str(ics_week_interval) + 'SA'

            if repeats != 'CUSTOM' and repeats is not None:
                ics_event.add('RRULE', {'FREQ': repeats, 'UNTIL': until})
            elif repeats == 'CUSTOM':
                ics_event.add('RRULE', {'FREQ': 'MONTHLY', 'UNTIL': until,'INTERVAL':1,'BYDAY':ics_week_interval})
            relist = []
            for ed_index in range(len(exdate)):
                #EXDATE;TZID=Pacific Standard Time:20230825T110000,20230707T110000
                date_format = str(exdate[ed_index]).replace('-','') + 'T' + str(time_from).replace(':','')
                relist.append(date_format)
            list_to_str = ','.join(relist)
            ics_event.add('exdate;TZID=Pacific Standard Time', list_to_str)
            ics_event.add('dtstamp', curr_date)
            ics_event.add('class', 'public')
            ics_event['location'] = vText(location)
            cal.add_component(ics_event)
            #need to escape forward slashes for the exdate ics output
            ics_file = cal.to_ical().decode("utf-8").replace("\\", "").replace('"', '')
            return ics_file

        title = self.title
        desc = strip_tags(self.description)
        start = datetime.datetime.combine(self.event_date, self.time_from)
        end = datetime.datetime.combine(self.event_date, self.time_to)
        event_date = self.event_date
        all_day = self.all_day
        time_from = self.time_from
        all_day = self.all_day
        curr_date = datetime.datetime.now()
        if self.until is not None:
            until = datetime.datetime.combine(self.until, self.time_to).astimezone(pytz.UTC)
        else:
            until = ''
        repeats = self.repeats
        ics_weekday = self.weekday
        ics_week_interval = self.week_interval
        exdate = [ed.exception_date for ed in self.exception_dates.all()] 
        location = self.location

        if "format" in request.GET:
            if request.GET['format'] == 'ical':
                #show the current url plus /ics
                response = HttpResponse(
                create_ical(title, desc, start, end, until, curr_date, repeats, ics_week_interval, ics_weekday, time_from, exdate, location, all_day, event_date),
                content_type='text/calendar',
                )
                response['Content-Disposition'] = 'attachment; filename=' + self.slug + '.ics'
                return response
            else:
                # Unrecognised format error
                message = 'Could not export event\n\nUnrecognised format: ' + request.GET['format']
                return HttpResponse(message, content_type='text/plain')

        def registration():
            if request.method == 'POST' and self.registration_form_chooser is not None and self.enable_registration == True:
                registration_form_page = RegistrationFormPage.objects.get(pk=self.registration_form_chooser)
                registration_form = registration_form_page.get_form(request.POST, request.FILES, page=self, user=request.user)                
                if registration_form.is_valid() and reg_spots_remaining > 0:
                    form_submission = registration_form_page.process_form_submission(registration_form)
                    user_id = get_primary
                    registration = Registration(event_name=event_id, user_info_id=get_primary[0], wait_list=0)
                    registration.save()
                    #messages.success(request, 'You have succesfully registered for ' + self.title)
                    status = 'registered'
                    #email function here
                    submission_email = registration_form.cleaned_data['email']
                    subject = 'You have succesfully registered for ' + self.title
                    plain_message = strip_tags(self.success_email_msg)
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [submission_email]
                    if from_email !='' and self.enable_email == True:
                        send_mail(subject, plain_message, from_email, [submission_email], html_message=self.success_email_msg)

                elif registration_form.is_valid() and reg_spots_remaining == 0 and wait_list_remaining > 0:
                    form_submission = registration_form_page.process_form_submission(registration_form)
                    user_id = get_primary
                    registration = Registration(event_name=event_id, user_info_id=get_primary[0], wait_list=1)
                    registration.save()
                    #messages.success(request, 'You have been added to the waitlist for ' + self.title)
                    status = 'waitlisted'
                    submission_email = registration_form.cleaned_data['email']
                    subject = 'You have been added to the wait listed for ' + self.title
                    plain_message = strip_tags(self.success_email_msg)
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [submission_email]
                    if from_email !='' and self.enable_email == True:
                        send_mail(subject, plain_message, from_email, [submission_email], html_message=self.success_email_msg)
                
            elif self.registration_form_chooser is not None:
                registration_form_page = RegistrationFormPage.objects.get(pk=self.registration_form_chooser)
                registration_form = registration_form_page.get_form(page=self, user=request.user)
                status = ''
            elif self.registration_form_chooser is None:
                status = ''
                registration_form = ''
            return registration_form, status
        registration_form, status = registration()
        if status == 'registered':
            return redirect(self.success_page.url)
        if status == 'waitlisted':
            return redirect(self.success_page.url)
        if status == '':
            return render(request, 'library_programs/event.html', {
                'page': self,
                'event_date_time_to': event_date_time_to,
                'until_date_time_to': until_date_time_to,
                'registration_form': registration_form,
                'reg_spots_remaining': reg_spots_remaining,
                'wait_list_remaining': wait_list_remaining,
            })

    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel('title'),
            FieldPanel('event_date'),
            FieldPanel('all_day'),
            FieldPanel('time_from'),
            FieldPanel('time_to'),
            FieldPanel('repeats'),
            FieldRowPanel(
            [
            FieldPanel("week_interval", classname="collapsed"),
            FieldPanel("weekday", classname="collapsed"),
            ],
            heading="Monthly Weekday Interval",
            classname="week-interval-display",
            ),
            FieldPanel('until'),
            #FieldPanel('repeating_dates'),
            InlinePanel('exception_dates', label="Exception Dates"),
            FieldPanel('event_category'),
            MultiFieldPanel(
            [
            FieldPanel("age_range", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Age Range"
            ),
            FieldPanel('description'),
            FieldPanel('event_image'),
            FieldPanel('location'),
            FieldPanel('tutorial_link'),
            FieldPanel('featured_on_home_page'),
    ], heading = "Program Info"), 
        ObjectList([
            FieldPanel('enable_registration'),
            FieldPanel('spots_available', classname="full"),
            FieldPanel('wait_list_spots', classname="full"),
            FieldPanel('close_reg_date'),
            PageChooserPanel('registration_form_chooser', ['library_programs.RegistrationFormPage']),
            PageChooserPanel('success_page'),
            MultiFieldPanel([
                FieldPanel('enable_email'),
                FieldPanel('success_email_msg'),
                FieldPanel('waitlist_email_msg'),
                ], heading="email settings")
           
            ], heading="Registration Setup"),
        ObjectList(Page.promote_panels, heading='Promote'),
        ])

    base_form_class =  EventEditExtraValidation

    def total_registered(self):
        total_registered = Registration.objects.filter(event_name_id=self.page_ptr_id, wait_list=0).count()
        return total_registered

    def total_spaces(self):
        return self.spots_available

    def spaces_remaining(self):
        total_registered = Registration.objects.filter(event_name_id=self.page_ptr_id, wait_list=0).count()
        spaces_remaining = self.spots_available - total_registered
        return spaces_remaining

    def waitlist_spots(self):
        return self.wait_list_spots

    def waitlist_remaining(self):
        current_waitlisted = Registration.objects.filter(event_name_id=self.page_ptr_id, wait_list=1).count()
        waitlist = self.wait_list_spots - current_waitlisted
        return waitlist

class ExceptionDate(models.Model) :
    event = ParentalKey(Event, on_delete=models.CASCADE, related_name='exception_dates')
    exception_date = models.DateField()

    def __str__(self):
        return self.exception_date

RESERVED_LABELS = ['Email']

def validate_label(value):
    if value in RESERVED_LABELS:
        raise ValidationError("'%s' is reserved." % value)

class RegistrationFormField(AbstractFormField):
    form_builder_page = ParentalKey('RegistrationFormPage', on_delete=models.CASCADE, related_name='form_fields')
    label = models.CharField(
        verbose_name='label',
        max_length=255,
        help_text='The label of the form field, cannot be one of the following: %s.'
        % ', '.join(RESERVED_LABELS),
        validators=[validate_label]
    )

#registration classes
class RegistrationFormPage(HoneypotFormMixin, HoneypotFormSubmissionMixin):

    content_panels = AbstractForm.content_panels + [
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="Form fields"),
    ]

    def get_submission_class(self):
        return RegistrationUserFormBuilder

    def process_form_submission(self, form):
        create_submission = self.get_submission_class().objects.create(form_data=form.cleaned_data, page=self)
        get_submission = self.get_submission_class().objects.filter(pk=create_submission.id).values('id')
        global get_primary
        get_primary = [id['id'] for id in get_submission]

    def get_form_fields(self):

            fields = list(super(RegistrationFormPage, self).get_form_fields())

            fields.insert(-1, RegistrationFormField(
                label='Email',
                field_type='email',
                required=True,
                help_text="Your email address"))

            return fields

    honeypot_panels = [
        MultiFieldPanel(
            [FieldPanel("honeypot")],
            heading="Reduce Form Spam",
        )
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(honeypot_panels, heading="Honeypot"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

    class Meta:
        verbose_name = "Registration Form Builder"

class RegistrationUserFormBuilder(AbstractFormSubmission):
    def parsed_form_data(self):
        try:
            data = super().get_data()
            print(data)
            def pretty_label(label):
                return label.replace("_", " ").capitalize()
        
            return format_html(
                "<ul>{}</ul>",
                format_html_join(
                    "",
                    "<li><strong>{}</strong>: {}</li>",
                    (
                        (pretty_label(k), v)
                        for k, v in data.items()
                        ),
                    ),
                )
        except Exception as e:
            return f"Invalid data ({e})"

    parsed_form_data.short_description = "Form Data"

class Registration(models.Model):
    user_info = models.ForeignKey('RegistrationUserFormBuilder', default=1, on_delete=models.CASCADE)
    event_name = models.ForeignKey('Event', default=1, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True, blank=True)
    wait_list = models.BooleanField(default=0)

    def email(self):
        email = self.user_info.form_data
        return email.get('email', None)

    def wait_listed(self):
        if self.wait_list == True:
            return 'Yes'
        elif self.wait_list == False:
            return 'No'

    def __str__(self):
        return self.event_name.title

    class Meta:
        verbose_name = "Registration"