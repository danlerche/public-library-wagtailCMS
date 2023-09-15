from django.db import models
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel, PageChooserPanel
from wagtail.fields import RichTextField
from wagtail.admin.forms import WagtailAdminPageForm
import datetime, json, pytz
from datetime import timedelta
from django import forms
from dateutil.rrule import *
from dateutil.parser import *
from django.utils.html import strip_tags
from django.http import HttpResponse
from icalendar import Calendar, Event, Alarm
from icalendar import Event as icsEvent, vDatetime, vText


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

class EventRepeats(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()
        # make sure that if repeats is selected that the user has also entered something in the until field
        repeats = cleaned_data['repeats']
        until = cleaned_data['until']
        week_interval = cleaned_data['week_interval']
        weekday = cleaned_data['weekday']
        if repeats is not None and until is None:
            self.add_error('until', 'please enter an until date or deselect the repeats option')
        elif repeats == 'CUSTOM' and week_interval is None:
            self.add_error('week_interval', 'Week interval cannot be blank if Custom is selected')
        elif repeats == 'CUSTOM' and weekday is None:
            self.add_error('weekday', 'Weekday cannot be blank if Custom is selected')
        return cleaned_data

    def save(self, commit=True):
        page = super().save(commit=False)
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
    time_from = models.TimeField(null=True)
    time_to = models.TimeField(null=True)
    description = RichTextField(max_length=1500,null=True,blank=True)
    repeats = models.CharField(max_length = 20, choices = REPEAT_CHOICE, null=True, blank=True)
    until = models.DateField(null=True,blank=True)
    week_interval = models.IntegerField(choices = WEEK_INTERVAL_CHOICE, null=True, blank=True)
    weekday = models.CharField(max_length = 20, choices = WEEKDAY_CHOICE, null=True, blank=True)
    event_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL,related_name='+')
    featured_on_home_page = models.BooleanField(default=False)
    repeating_dates = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True, help_text="Enter a location where the event will happen")
    form_page = models.ForeignKey('wagtailcore.Page', blank=True, null=True, on_delete=models.SET_NULL, related_name='embedded_form_page', help_text='Select a Form that will be embedded on this page.')
    tutorial_link = models.CharField(max_length=255, blank=True, help_text="for showing Niche Academy Links or similar")

    #allows web forms to be included at the bottom of the page
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        #Add a renderable form to the page's context if form_page is set
        if self.form_page:
            form_page = self.form_page.specific  
            # must get the specific page
            # form will be a renderable form as per the dedicated form pages
            form = form_page.get_form(page=form_page, user=request.user)
            context['form'] = form
            context['form_page'] = form_page
            #create an event_date_time template tag. Used for the "this event is in the past message"
        event_date_time_to = datetime.datetime.combine(self.event_date, self.time_to)
        if self.until is not None: 
            until_date_time_to = datetime.datetime.combine(self.until, self.time_to)
        else:
            until_date_time_to = ''
        context['event_date_time_to'] = event_date_time_to
        context['until_date_time_to'] = until_date_time_to
        return context
        
    #function to generate .ics files for integration into calendars
    def serve(self, request):
        def create_ical(title, desc, start, end, until, curr_date, repeats, ics_week_interval, ics_weekday, time_from, exdate, location):
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
        time_from = self.time_from
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
                create_ical(title, desc, start, end, until, curr_date, repeats, ics_week_interval, ics_weekday, time_from, exdate, location),
                content_type='text/calendar',
                )
                response['Content-Disposition'] = 'attachment; filename=' + self.slug + '.ics'
                return response
            else:
                # Unrecognised format error
                message = 'Could not export event\n\nUnrecognised format: ' + request.GET['format']
                return HttpResponse(message, content_type='text/plain')
        else:
            # Display event page as usual
            return super().serve(request)

    content_panels = Page.content_panels + [
    FieldPanel('event_date'),
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
    FieldRowPanel(
            [
                PageChooserPanel('form_page', ['webform.FormPage']),
            ],
            heading="Optional Form Page",
        ),
    FieldPanel('featured_on_home_page'),
    ]
    base_form_class =  EventRepeats

class ExceptionDate(models.Model) :
    event = ParentalKey(Event, on_delete=models.CASCADE, related_name='exception_dates')
    exception_date = models.DateField()

    def __str__(self):
        return self.exception_date
