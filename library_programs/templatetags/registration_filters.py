from django import template
register = template.Library()

@register.filter(name="und_to_space")
def und_to_space(value):
    #replaces all underscores with spaces
    return value.replace("_", " ")