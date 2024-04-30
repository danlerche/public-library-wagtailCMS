from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
import datetime
from django.db.models import Count
from django.db.models.functions import ExtractYear
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.blocks import BlockQuoteBlock

# Create your models here.

class newsIndexPage(RoutablePageMixin, Page):
	intro = RichTextField(blank=True)

	@path('')
	def news_items(self, request):
		news_items = newsItem.objects.all().live().order_by('-news_date')
		news_count_by_year = newsItem.objects.annotate(year=ExtractYear('news_date')).values('year').annotate(count=Count('id')).order_by('-year')
		
		return self.render(request, context_overrides={
			'news_items': news_items, 
			'news_count_by_year': news_count_by_year,
		})

	@path('<int:year>/')
	def events_for_year(self, request, year=None):
		"""
		View function for the events for year page
		"""
		if year is None:
			year = datetime.date.today().year

		news_items = newsItem.objects.live().filter(news_date__year=year)

		news_count_by_year = newsItem.objects.annotate(year=ExtractYear('news_date')).values('year').annotate(count=Count('id')).order_by('-year')

		current_url = self.url_path[len("/home"):]

		return self.render(request, context_overrides={
			'news_items': news_items,
			'current_url': current_url,
			'news_count_by_year': news_count_by_year,
 		})

	content_panels = Page.content_panels + [
		FieldPanel('intro'),
	]

class newsItem(Page):
	news_date = models.DateField(default=datetime.date.today)
	news_image = models.ForeignKey('wagtailimages.Image', blank=False, null=True, help_text="upload an image for the bio", on_delete=models.SET_NULL,related_name='+')

	content = StreamField([
		('quote', BlockQuoteBlock(required=True, help_text="Enter the text you'd like to appear in quotation marks")),
		('paragraph', blocks.RichTextBlock()),
		], use_json_field=True, blank=True)
	
	content_panels = Page.content_panels + [
        FieldPanel('news_date'),
		FieldPanel('news_image'),
		FieldPanel('content'),
	]