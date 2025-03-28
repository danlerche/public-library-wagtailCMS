from django.shortcuts import redirect
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel, PageChooserPanel
)
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.admin.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils.html import strip_tags
from wagtail.admin.panels import TabbedInterface, ObjectList
from wagtail.models import Page

from wagtail_honeypot.models import (
    HoneypotFormMixin, HoneypotFormSubmissionMixin
)

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(HoneypotFormMixin, HoneypotFormSubmissionMixin):
    intro = RichTextField(blank=True)
    send_copy = models.BooleanField(default=False)
    thank_you_text = RichTextField(blank=True)

    thank_you_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    submit_button_text = models.TextField(blank=True, max_length=200)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        PageChooserPanel('thank_you_page'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
                FieldPanel('send_copy', help_text="send emailed copy of the form to the patron"),
            ]),
            FieldPanel('subject'),
            FieldPanel('thank_you_text', classname="full"),
            FieldPanel('submit_button_text', classname="full", heading="Submit Button Text (if blank, Submit will be used)"),
        ], "Email"),
    ]

    honeypot_panels = [
        MultiFieldPanel(
            [FieldPanel("honeypot")], heading="Reduce Form Spam",
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

    def render_landing_page(self, request, form_submission=None, *args, **kwargs):
        if self.thank_you_page:
            url = self.thank_you_page.url
            # if a form_submission instance is available, append the id to URL
            # when previewing landing page, there will not be a form_submission instance
            if form_submission:
                ty_text = strip_tags(self.thank_you_text)
                messages.info(request, ty_text)
                url += '?id=%s' % form_submission.id
            return redirect(url, permanent=False)
        # if no thank_you_page is set, render default landing page
        return super().render_landing_page(request, form_submission, *args, **kwargs)
        
    def send_mail(self, form):
        # `self` is the FormPage, `form` is the form's POST data on submit

        # Email addresses are parsed from the FormPage's addresses field
        email_key = 'email'
        if self.send_copy == 1 and email_key in form.data.keys():
            form_email_field = [form['email'].data]
            to_address = [x.strip() for x in self.to_address.split(',')]
            for addr in to_address: 
                form_email_field.append(addr)
                addresses = form_email_field
        else: 
            addresses = [x.strip() for x in self.to_address.split(',')]
        
        subject = self.subject

        send_mail(subject, self.render_email(form), addresses, self.from_address,)

        #csv export

        def get_data_fields(self):
            data_fields = [
                ('username', 'Username'),
            ]
            data_fields += super().get_data_fields()

            return data_fields

class CustomFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_data(self):
        form_data = super().get_data()
        form_data.update({
            'username': self.user.username,
        })

        return form_data