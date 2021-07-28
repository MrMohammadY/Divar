from django import template

register = template.Library()


@register.simple_tag()
def get_mark_advertisement(user, advertisement_id):
    mark = user.marks.filter(advertisement=advertisement_id)
    if mark.exists():
        return True
    return False
