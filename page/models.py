from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.blocks import DateBlock, DateTimeBlock, URLBlock, EmailBlock, TimeBlock, StreamBlock, ChoiceBlock, MultipleChoiceBlock
from wagtail.blocks import DateTimeBlock, TimeBlock, BlockQuoteBlock, PageChooserBlock, ListBlock, BooleanBlock, TextBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.search import index
from wagtail.embeds.oembed_providers import youtube, vimeo
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from unidecode import unidecode
from django.template import defaultfilters
from library_programs.models import EventCategory, EventAudience
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from django import forms
from wagtail.admin import widgets
from django.shortcuts import redirect
from django.utils.html import format_html
from wagtail.models.media import Collection
from wagtail.admin.forms import WagtailAdminPageForm
from django.conf import settings

class groupPage(Page):
    pass

class GoogleMapBlock(blocks.StructBlock):
    place_name = blocks.CharBlock(label="Place Name", required=True)
    address = blocks.TextBlock(label="Address", required=True)
    zoom = blocks.IntegerBlock(label="Zoom Level", default=15)

    class Meta:
        icon = 'map'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['place_name'] = value['place_name']
        context['address'] = value['address']
        context['zoom'] = value['zoom']
        context['api_key'] = getattr(settings, 'GOOGLE_MAP_API_KEY')
        return context

    def render(self, value, *args, **kwargs):
        return super().render(value, *args, **kwargs)

class OpenStreetMapBlock(blocks.StructBlock):
    place_name = blocks.CharBlock(label="Place Name", required=True)
    latitude = blocks.FloatBlock()
    longitude = blocks.FloatBlock()
    zoom = blocks.IntegerBlock(label="Zoom Level", default=19)

    class Meta:
        icon = 'map'  # Choose an appropriate icon

class PolicyCategory(models.Model):
    policy_category = models.CharField(max_length=255)

    panels = [
        FieldPanel('policy_category'),
    ]

    def __str__(self):
        return self.policy_category

    class Meta:
        verbose_name_plural = 'Policy categories'


class PolicyIndexPage(Page):
    additional_text = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        policy_pages = self.get_children().live()
        context['policy_pages'] = policy_pages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('additional_text', classname="full")
    ]

def get_categories():
    return [(cat.id, cat.category_name) for cat in EventCategory.objects.all()]
def get_audiences():
    return [(aud.id, aud.audience_name) for aud in EventAudience.objects.all()]
def get_collection():
    return [(col.id, col.name) for col in Collection.objects.all()]

class AllPurposePage(Page):
# tutorial to add web forms to the pages. Not a stream form but who cares https://stackoverflow.com/questions/48636619/wagtail-feedback-form-in-homepage

    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image_link', blocks.StructBlock([
            ('image_link_url', URLBlock(help_text="The Link to redirect to")),
            ('image', ImageChooserBlock(help_text="The image the user will see")),
        ], template='page/blocks/image_link.html', icon='openquote')),
        ('half_size_image', ImageChooserBlock(help_text="Takes up 1/2 of the screen size 648px")),
        ('full_width_image', ImageChooserBlock(help_text="Takes up the full screen view 1248px")),
        ('image', ImageChooserBlock(help_text="uses the original picture size and respects that with")),
        ('image_w_accessible_heading', ImageChooserBlock(help_text="uses the original picture size and puts an additional h2 heading for accessibility")),
        ('card', blocks.StructBlock([
        ('card_body', blocks.StreamBlock([
            ('card_item', blocks.StructBlock(
                [  
                    ('card_image', ImageChooserBlock(required=True)),
                    ('card_page', PageChooserBlock(required=False)),
                    ('card_external_url', URLBlock(required=False, help_text="use this if you're directing to an extenal page")),
                    ('card_alt_title', blocks.CharBlock(required=False, help_text="use the alt title for external URLs or override the name of the page it's linking to")),
                    ('card_description', blocks.CharBlock(required=False, help_text="This is optional, but better to be consisiten with each of your cards")),
                ], template='page/blocks/card_item.html', icon='placeholder')),
            ]))
            ], template='page/blocks/card.html', icon='image')),
        ('image_carousel', ChoiceBlock(choices=get_collection, required=False, help_text="Select an image collection to show as a slideshow", icon='image')),
        ('QuoteBlock', blocks.StructBlock([
            ('quote', BlockQuoteBlock(required=True, help_text="Enter the text you'd like to appear in quotation marks")),
            ('attribution', blocks.CharBlock(required=False, help_text="attribute the quote to someone")),
        ], template='page/blocks/block_quote.html', icon='openquote')),
        ('text_only_table', TableBlock()),
        ('richtext_table', TypedTableBlock([
            ('rich_text', blocks.RichTextBlock()),
        ])),
        ('URLBlock', URLBlock()),
        ('EmailBlock', EmailBlock()),
        ('all_upcoming_events', BooleanBlock(required=False, help_text="If checked a list of upcoming events will display", icon='tasks')),
        ('events_calendar', BooleanBlock(required=False, help_text="If checked an event calendar will display", icon='tasks')),
        ('events_by_category', MultipleChoiceBlock(choices=get_categories, 
            required=False, help_text="If checked all upcoming programs filtered by a category will display", icon='tasks')),
        ('events_by_audience', MultipleChoiceBlock(choices=get_audiences, 
            required=False, help_text="If checked all upcoming programs filtered by a audiences will display", icon='tasks')),
        ('DateBlock', DateBlock()),
        ('TimeBlock', TimeBlock()),
        ('DateTimeBlock', DateBlock()),
        ('PageChooserBlock', PageChooserBlock()),
        ('DocumentChooserBlock', DocumentChooserBlock()),
        ('IframeBlock', blocks.RawHTMLBlock(help_text="See https://search.pentictonlibrary.ca/Admin/CollectionSpotlights for info about using the iframe tag to embed Aspen Collection Spotlights.")),
        ('PhoneNumberBlock', TextBlock()),
        ('EmbedBlock', EmbedBlock()),
        #('google_map', GoogleMapBlock(template='page/blocks/google_map_block.html', icon='globe')),
        #('open_street_map', OpenStreetMapBlock(template='page/blocks/openstreetmap_block.html', icon='site')),
        ('show_business_hours', BooleanBlock(required=False, help_text="If checked, the library hours will display on the page", icon='user')),
        ('show_next_closure', BooleanBlock(required=False, help_text="If checked, the next library closure will display", icon='user')),
        ('show_all_closures', BooleanBlock(required=False, help_text="If checked, all upcoming library closures will be shown", icon='user')),
        ('bookClub', blocks.StructBlock([
            ('book_club_name', blocks.CharBlock()),
            ('book_club_day_of_the_week', blocks.TextBlock()),
            ('book_club_PDF', DocumentChooserBlock(required=False)),
            ('book_club_time', blocks.TimeBlock()),
            ('books', blocks.StreamBlock(
                [
                    ('book', blocks.StructBlock([
                        ('book_name', blocks.CharBlock()),
                        ('author_name', blocks.CharBlock()),
                        ('reading_date', blocks.DateBlock()),
                        ('book_description', blocks.RichTextBlock()),
                        ('book_cover', ImageChooserBlock(required=False)),
                    ],template='page/blocks/books.html'),),
                ]
            )),
            ], template='page/blocks/book_club.html', icon='openquote')),
        ('columnBlock', blocks.StructBlock([
            ('column', blocks.StreamBlock([
                ('richtext', blocks.RichTextBlock()),
                ('image', ImageChooserBlock(required=False)),
                ('quote_block', blocks.StructBlock([
                    ('quote', BlockQuoteBlock(required=True, help_text="Enter the text you'd like to appear in quotation marks")),
                    ('attribution', blocks.CharBlock(required=False, help_text="attribute the quote to someone")),
                    ], template='page/blocks/block_quote.html', icon='openquote')),
            ]))
        ],template='page/blocks/column.html', icon='table')),
        ('ebooks_card', blocks.StructBlock([
        ('ebooks_body', blocks.StreamBlock([
            ('ebook', blocks.StructBlock(
                [   ('ebook_title', blocks.CharBlock(required=True)),
                    ('ebook_url', URLBlock()),
                    ('ebook_image', ImageChooserBlock(required=True)),
                    ('ebook_description', blocks.RichTextBlock(required=False, help_text="OPTIONAL, only use this if you'd like to override the name of the page you are linking to")),
                    ('tutorial_link', blocks.CharBlock(required=False, help_text="use the short codes from Niche academy")),
                    ('app_link', blocks.StreamBlock([
                        ('app_links', blocks.StructBlock([
                            ('bootstrap_app_icon', blocks.CharBlock(required=False, help_text="See https://icons.getbootstrap.com for icon codes")), 
                            ('app_link', blocks.URLBlock(required=False, help_text="url to the app store link")),
                            ('app_icon_description', blocks.CharBlock(required=True, help_text="a short description of the app you are linking to")),
                            ], template='page/blocks/app_link.html', icon='site'))
                        ], required=False))
                ], template='page/blocks/ebook.html', icon='openquote')),
            ]))
            ], template='page/blocks/ebooks_card.html', icon='image')),
        ('side_menu', blocks.StructBlock([
        ('side_menu_title', blocks.CharBlock()),
        ('side_menu_body', blocks.StreamBlock([
            ('side_menu_item', blocks.StructBlock(
                [   ('page_link', PageChooserBlock(required=False)),
            ('pdf_document', DocumentChooserBlock(required=False)),
            ('external_url', blocks.URLBlock(required=False)),
            ('external_url_link_title', blocks.CharBlock(required=False)),
                ], template='page/blocks/side_menu_item.html', icon='openquote')),
            ]))
            ],template='page/blocks/side_menu.html', icon='collapse-down')),
        ('accordion', blocks.StructBlock([
            ('accordion_name', blocks.CharBlock()),
            ('only_one_open', blocks.BooleanBlock(required=False, default=True, help_text="Automatically close all other accordions while another is open")),
            ('accordion_body', blocks.StreamBlock(
                [
                    ('accordion_items', blocks.StructBlock([
                        ('accordion_item_title', blocks.CharBlock()),
                        ('accordion_description', blocks.RichTextBlock()),
                        ('show_by_default', blocks.BooleanBlock(required=False, help_text="Display accordion as open by default")),
                    ]),),
                ]
            )),
            ], template='page/blocks/accordion.html', icon='collapse-down')),
    ], use_json_field=True, blank=True)

    policy_category = models.ForeignKey(PolicyCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='pol_cat')
    form_page = models.ForeignKey('wagtailcore.Page', blank=True, null=True, on_delete=models.SET_NULL, related_name='form_page_embed', help_text='Select a Form that will be embedded on this page.')

    #allows webforms to be included at the bottom of the page
    def get_context(self, request, *args, **kwargs):
        """Add a renderable form to the page's context if form_page is set."""
        context = super().get_context(request, *args, **kwargs)
        if self.form_page:
            form_page = self.form_page.specific  
            # must get the specific page
            # form will be a renderable form as per the dedicated form pages
            form = form_page.get_form(page=form_page, user=request.user)
            context['form'] = form
            context['form_page'] = form_page
        return context

    # you can create them separately
    select_widget = forms.Select(
        attrs = {
            'placeholder': 'Select an optional policy category'
        }
    )

    content_panels = Page.content_panels + [
        FieldPanel('content'),
        FieldPanel('policy_category', widget=select_widget,  help_text='select an optional policy category'),
        FieldRowPanel(
            [
                PageChooserPanel('form_page', ['webform.FormPage']),
            ],
            heading="Optional Form Page",
        ),
    ]

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]

class RedirectValidationForm(WagtailAdminPageForm):

    def clean(self):
        cleaned_data = super().clean()
        # Make either the internet or external url is filled, not both
        redirect_to = cleaned_data['redirect_to']
        redirect_to_page = cleaned_data['redirect_to_page']
        if redirect_to is not None and redirect_to_page is not None:
            self.add_error('redirect_to_page', "Please only choose an internal page or an extenal URL, not both.")
            self.add_error('redirect_to', "Please only choose an internal page or an extenal URL, not both.")
        elif redirect_to is None and redirect_to_page is None:
            self.add_error('redirect_to', "No selection made. Please choose an internal page, or an extenal URL")
            self.add_error('redirect_to_page', "No selection made. Please choose an internal page, or an extenal URL")
        return cleaned_data

class RedirectorPage(Page):
    
    redirect_to_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        )
    redirect_to = models.URLField(
        null=True,
        blank=True,
        help_text='The URL to redirect to',
        max_length=2000
    )

    content_panels = Page.content_panels + [
        FieldPanel('redirect_to_page', classname="full"),
        FieldPanel('redirect_to', classname="full"),
    ]

    base_form_class = RedirectValidationForm

    def get_admin_display_title(self):
        if self.redirect_to is not None:
            return format_html(f"{self.draft_title}<br/>➡️ {self.redirect_to}")
        else:
            return format_html(f"{self.draft_title}<br/>Redirects to: ➡️ {self.redirect_to_page}")

    class Meta:
        verbose_name = 'Redirector'

    def serve(self, request):
        if self.redirect_to is not None:
            return redirect(self.redirect_to)
        else:
            return redirect(self.redirect_to_page.url)