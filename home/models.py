from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail import blocks
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import BooleanBlock
from wagtail.blocks import PageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

class HomePage(Page):
    content = StreamField([
        ('background_image_w_searchbar', ImageChooserBlock(template='home/blocks/background_image_w_searchbar.html', icon='collapse-down')),
        ('aspen_carousel', blocks.StructBlock([
            ('aspen_carousel_title', blocks.CharBlock(required=True, help_text="The title of the carousel to be displayed on the homepage")),
            ('aspen_iframetag', blocks.CharBlock(required=True, template='home/blocks/aspen_carousel.html', icon='collapse-down', help_text="requires an Aspen Discovery iframe tag. Go to https://search.pentictonlibrary.ca/Admin/CollectionSpotlights for more info")),
        ], template='home/blocks/aspen_carousel.html')),
        ('upcoming_events_features', BooleanBlock(required=False, default=1, help_text="If checked BOTH the three program features plus an upcoming events list row will display", icon='tasks')),
        ('single_feature', blocks.StructBlock([
            ('page', blocks.PageChooserBlock(required=False, help_text="The internal page to link to")),
            ('single_feature_image', ImageChooserBlock(required=False)),
            ('single_feature_video_embed', blocks.RawHTMLBlock(required=False, help_text="Embed a video using an iframe tag provided by youTube, or another source instead of displaying the image.")),
            ('single_feature_description', blocks.CharBlock(required=True, help_text="write a short description of the feature")),
            ('override_title', blocks.CharBlock(required=False, help_text="OPTIONAL, only use this if you'd like to override the name of the page you are linking to")),
            ('enabled', blocks.BooleanBlock(default=True, required=False))
            ], template='home/blocks/single_feature.html', icon='image'),),
        ('feature_row', blocks.StructBlock([
        ('feature_row_title', blocks.CharBlock(required=True, help_text="Pick a title for your list of features")),
        ('feature_body', blocks.StreamBlock([
            ('feature', blocks.StructBlock(
                [
                    ('page', blocks.PageChooserBlock(required=False, help_text="The internal page to link to")),
                    ('feature_document', DocumentChooserBlock(required=False, help_text="OPTIONAL: use this to link to a PDF document instead of a page")),
                    ('feature_image', ImageChooserBlock(required=True)),
                    ('feature_text', blocks.CharBlock(required=False, help_text="OPTIONAL, only use this if you'd like to override the name of the page you are linking to")),
                ], template='home/blocks/feature.html', icon='openquote')),
            ]))
            ], template='home/blocks/feature_row.html', icon='image')),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content'),
        ]
