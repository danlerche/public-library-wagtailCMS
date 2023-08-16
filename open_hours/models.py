from django.db import models
from wagtail.snippets.models import register_snippet
from django import forms
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
import datetime

class EnableMessageDisplay(models.Model):
    enable_message_display = models.BooleanField(default=1, null=False, help_text="uncheck to hide the open and closed hours display")

    panels = [
        FieldPanel('enable_message_display'),
    ]


    def __str__(self):
        return 'Enable Message'

class SocialMedia(models.Model):
    social_media_name = models.CharField(max_length=200, null=True, blank=True)
    social_media_link = models.CharField(max_length=200, null=True, blank=True)
    social_media_icon = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.social_media_name

    panels = [
        FieldPanel('social_media_name'),
        FieldPanel('social_media_link'),
        FieldPanel('social_media_icon'),
    ]

class BranchInfo(models.Model):
    branch_name = models.CharField(max_length=200, null=True, blank=True)
    hours_page = models.ForeignKey('wagtailcore.Page',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',)
    closed_holiday_page = models.ForeignKey('wagtailcore.Page',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',)
    street_number = models.SmallIntegerField(null=True, blank=True)
    street_name = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    province_state = models.CharField(max_length=2, null=True, blank=True)
    postal_code = models.CharField(max_length=7, null=True, blank=True)
    telephone = models.CharField(max_length=14, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    social_media = models.ManyToManyField("SocialMedia")

    panels = [
        FieldPanel('branch_name'),
        FieldPanel('hours_page'),
        FieldPanel('closed_holiday_page'),
        FieldPanel('street_number'),
        FieldPanel('street_name'),
        FieldPanel('city'),
        FieldPanel('province_state'),
        FieldPanel('postal_code'),
        FieldPanel('telephone'),
        FieldPanel('email'),
        FieldPanel('social_media'),
    ]

    def __str__(self):
        return self.branch_name

class OpenHourValidationForm(WagtailAdminPageForm):

    def clean(self):
        cleaned_data = super().clean()

        # Make sure start time is before end time
        time_from= cleaned_data['time_from']
        time_to = cleaned_data['time_to']
        if time_from and time_to and time_from > time_to:
            self.add_error('time_to', "Let's not bend time here. Start time is past end time")
        return cleaned_data

class OpenHour(models.Model):
    branch_info = models.ForeignKey(BranchInfo, on_delete=models.SET_NULL, null=True, default=1)
    
    class WeekDayNames(models.IntegerChoices): 
        Monday = 0
        Tuesday = 1
        Wednesday = 2
        Thursday = 3
        Friday = 4
        Saturday = 5
        Sunday = 6
    day_of_the_week = models.SmallIntegerField(choices=WeekDayNames.choices)

    def weekday(self):
        return self.WeekDayNames(self.day_of_the_week).label

    class OpenClosed(models.IntegerChoices):
        Closed = 0
        Open = 1
    open_closed = models.BooleanField(choices=OpenClosed.choices, default=1)

    def open_or_closed(self):
        return self.OpenClosed(self.open_closed).label 
    
    time_from = models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
    time_to = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    open_hours_label = 'Open Hours'

    panels = [
        FieldPanel('branch_info'),
        FieldPanel('day_of_the_week'),
        FieldPanel('time_from'),
        FieldPanel('time_to'),
        FieldPanel('open_closed'),
        ]

    base_form_class = OpenHourValidationForm

    def __str__(self):
        return self.weekday()

class ClosedDate(models.Model):
    branch_info = models.ForeignKey(BranchInfo, on_delete=models.SET_NULL, null=True, default=1)
    closed_date_name = models.TextField(default="holiday")
    closed_date_from = models.DateField(default=datetime.date.today)
    closed_date_to = models.DateField(default=datetime.date.today)
    all_day = models.BooleanField(default=True, help_text="Default is checked. uncheck to have special holiday hours")
    time_from = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True, help_text="only takes effect if All Day is unchecked")
    time_to = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True, help_text="only takes effect if All Day is unchecked")
    closed_dates_label = 'Exception Dates and Hours'

    panels = [
        FieldPanel('branch_info'),
        FieldPanel('closed_date_name'),
        FieldPanel('closed_date_from'),
        FieldPanel('closed_date_to'),
        MultiFieldPanel(
        [
        FieldPanel('all_day'),
        FieldPanel('time_from'),
        FieldPanel('time_to'),
        ],
        heading = "Exception Hours",
        classname = "collapsible collapsed"
        ),
        ]
    def __str__(self):
        return self.closed_dates_label