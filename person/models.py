from django.db import models
from wagtail.models import Page
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import PageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

class PersonIndexPage(Page):
    intro = RichTextField(blank=True)
    side_menu = StreamField([
		('side_menu', blocks.StructBlock([
        ('side_menu_title', blocks.CharBlock()),
        ('side_menu_body', blocks.StreamBlock([
            ('side_menu_item', blocks.StructBlock(
                [ 
            ('pdf_document', DocumentChooserBlock(required=False)),
                ], template='person/blocks/side_menu_item.html', icon='openquote')),
            ]))
            ],template='person/blocks/side_menu.html', icon='collapse-down')),
    	], use_json_field=True, blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        person_entries = self.get_children().live()
        context['person_entries'] = person_entries
        return context

    content_panels = Page.content_panels + [
    	FieldPanel('intro'),
    	FieldPanel('side_menu'),
    ]

class personEntry(Page):
    image = models.ForeignKey('wagtailimages.Image', blank=False, null=True, help_text="upload an image for the bio", on_delete=models.SET_NULL,related_name='+')
    introduction = models.CharField(max_length=165)
    biography = RichTextField(blank=False)
    position = models.CharField(max_length=200, null=True)
	
    content_panels = Page.content_panels + [
        FieldPanel('position'),
		FieldPanel('image'),
		FieldPanel('introduction'),
		FieldPanel('biography'),
	]