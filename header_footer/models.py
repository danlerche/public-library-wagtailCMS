from django.db import models
from datetime import datetime
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel,InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from wagtail.blocks import StaticBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import StreamField
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.blocks import (
  CharBlock, PageChooserBlock, StructValue, StructBlock, TextBlock, URLBlock, EmailBlock, BooleanBlock)
from open_hours.models import OpenHour, BranchInfo, SocialMedia
#from wagtailmenus.models.menus import FlatMenu

class Logo(models.Model):
    logo_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    logo_label = 'Logo'

    panels = [
       FieldPanel('logo_image', classname="full"),
    ]

    def __str__(self):
        return self.logo_label

class Alert(Orderable):
    enable_alert = models.BooleanField(default=True)
    alert_date = models.DateTimeField(default=datetime.now, help_text="The start of the alert")
    alert_end_date = models.DateTimeField(blank=True, null=True, help_text="If entered, the time the alert should be removed from public view")
    alert_text = RichTextField(blank=True)
    alert_label = 'Pop Up Alert'

    panels = [
        FieldPanel('enable_alert'),
        FieldPanel('alert_date'),
        FieldPanel('alert_end_date'),
        FieldPanel('alert_text'),
    ]

    def __str__(self):
        return self.alert_label

class TelephoneBlock(blocks.StructBlock):
        telephone = blocks.CharBlock(classname="telephone")
        class Meta:
            template = 'header_footer/blocks/telephone.html'

class HeadingBlock(blocks.StructBlock):
        heading = blocks.CharBlock(classname="heading")
        class Meta:
            template = 'header_footer/blocks/heading.html'

class EmailBlock(blocks.StructBlock):
        email = blocks.EmailBlock(classname="email")
        class Meta:
            template = 'header_footer/blocks/email.html'

class BranchInfoBlock(blocks.StaticBlock):
        def get_context(self, request):
            context = super().get_context(request)
            branch_info = BranchInfo.objects.all()
            context['branch_info'] = branch_info
            return context
        class Meta:
            template = 'open_hours/branch_info.html' 

class SocialIconsBlock(blocks.StaticBlock):
        def get_context(self, request):
            context = super().get_context(request)
            social_media = SocialMedia.objects.all()
            context['social_media'] = social_media
            return context
        class Meta:
            template = 'open_hours/social_icons.html' 

class BusinessHourBlock(blocks.StaticBlock):
        def get_context(self, request):
            context = super().get_context(request)
            business_hour = OpenHour.objects.all().order_by('day_of_the_week')
            branch_info = BranchInfo.objects.all()
            context['business_hour'] = business_hour
            context['branch_info'] = branch_info
            return context
        class Meta:
            template = 'open_hours/business_hours_footer.html'

class PageLinkBlock(blocks.StructBlock):
        page_link = blocks.PageChooserBlock()
        class Meta:
            template = 'header_footer/blocks/footer_page_link.html'

class ButtonBlock(blocks.StructBlock):
        button_link = blocks.PageChooserBlock()
        class Meta:
            template = 'header_footer/blocks/footer_button.html'

class FooterColumn(models.Model):
    footer_col_heading = 'Footer Column'
    order = models.IntegerField(null=True, blank=False, help_text="use incrementally to order the footer columns from left to right")
    footer_col = StreamField([
        ('heading', HeadingBlock(classname="full title")),
        ('table', TableBlock()),
        ('footer_link', PageLinkBlock()),
        ('footer_button', ButtonBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('telephone', TelephoneBlock()),
        ('image', ImageChooserBlock()),
        ('email', EmailBlock()),
        ('branch_info', BranchInfoBlock()),
        ('business_hours', BusinessHourBlock()),
        ('social_icons', SocialIconsBlock()),

    ], use_json_field=True, blank=True)

    class Meta:
        verbose_name = "First Footer Column"
    def __str__(self):
        return self.footer_col_heading

    panels = [
        FieldPanel('order'),
        FieldPanel('footer_col'),
    ]