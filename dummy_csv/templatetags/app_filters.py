from django import template
from django.forms import BoundField

register = template.Library()


@register.filter
def add_place_holder(field, place_holder=None):
    if place_holder is None:
        return field
    else:
        field.field.widget.attrs.update({'placeholder': place_holder})
        return field


@register.filter
def add_class(field, class_name):
    if isinstance(field, BoundField):
        field.field.widget.attrs.update({'class': class_name})
    return field
