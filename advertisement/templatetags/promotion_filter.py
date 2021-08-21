from django import template

from promotion.models import Promotion

register = template.Library()


@register.simple_tag()
def promotion_instantaneous(advertisement):
    advertisement_promotion = advertisement.promotions.filter(promotion__name=Promotion.INSTANTANEOUS).last()
    if advertisement_promotion is None:
        return False
    return advertisement_promotion.cal_inst()
