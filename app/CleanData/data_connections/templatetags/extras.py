from django import template
register = template.Library()

@register.filter
def ofKey(value, arg):
    if value:
        return getattr(value,arg)
    else:
        return ""