from django import template

from advertisement.models import Category

register = template.Library()


@register.simple_tag()
def categories():
    return Category.objects.filter(parent=None)
