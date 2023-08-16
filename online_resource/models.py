from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from django import forms
from django.shortcuts import render

class OnlineResourceCategory(models.Model):
    name = models.CharField(max_length=255)
    category_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,related_name='+')

    panels = [
        FieldPanel('name'),
        FieldPanel('category_image'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'online resource categories'


class OnlineResourceIndexPage(Page):
    intro = RichTextField(blank=True)
    niche_academy = models.CharField(max_length=250, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        online_resource_pages = self.get_children().live().order_by('title')
        categories = OnlineResourceCategory.objects.all().order_by('name')
        #cat_id shoudl equal whatever value is checked off in the checkboxes
        #cat_id = request.GET.get('values from the checkboxes')
        #https://stackoverflow.com/questions/8259609/how-to-update-a-django-query-variable-using-ajax-query
        #https://stackoverflow.com/questions/19131800/getting-value-from-checked-checkbox-in-ajax
        #resource_by_category = OnlineResourcePage.objects.filter(categories__id=11).order_by('title')
        resource_by_category = OnlineResourcePage.objects.all().order_by('title')
        context['online_resource_pages'] = online_resource_pages
        context['categories'] = categories
        context['resource_by_category'] = resource_by_category
        return context


    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('niche_academy', classname="full"),
    ]


class OnlineResourcePage(Page):
    online_resource_url = models.CharField(max_length=400, blank=True)
    online_resource_description = RichTextField(blank=True)
    resource_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,related_name='+')
    categories = ParentalManyToManyField('online_resource.OnlineResourceCategory', blank=False, )
    tutorial_link = models.CharField(max_length=255, blank=True)
    featured = models.BooleanField(default=False)
    featured_description = RichTextField(blank=True, max_length=400) 

    content_panels = Page.content_panels + [
        FieldPanel('online_resource_url'),
        FieldPanel('online_resource_description'),
        FieldPanel('resource_image'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tutorial_link'),
        FieldPanel('featured'),
        FieldPanel('featured_description'),
    ]
