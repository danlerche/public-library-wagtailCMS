from django import template
from wagtail.images.models import Image

register = template.Library()
@register.inclusion_tag('page/get_images_by_collection.html', takes_context=True)
def get_images_by_collection(context, filter_by):
	request = context['request']
	images = Image.objects.filter(collection=filter_by)

	return { 'request': request, 
	'images': images,
	}