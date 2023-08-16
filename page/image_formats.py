# image_formats.py
from wagtail.images.formats import Format, register_image_format

register_image_format(Format('table-rounded', 'Richtext Table Rounded', 'img-fluid rounded', 'fill-200x200-c100'))
