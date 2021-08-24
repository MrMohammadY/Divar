from django.utils.translation import ugettext_lazy as _
from advertisement.models import *
from django.db import models


class Promotion(BaseModel):
    INSTANTANEOUS = 1
    LADDER = 2
    PROMOTION_TYPE = (
        (INSTANTANEOUS, 'instantaneous'),
        (LADDER, 'ladder'),
    )
    name = models.SmallIntegerField(verbose_name=_('name'), choices=PROMOTION_TYPE)
    price = models.IntegerField(verbose_name=_('price'))

    def __str__(self):
        return f'{self.get_name_display()}'


class AdvertisementPromotion(BaseModel):
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name='promotions',
        verbose_name=_('advertisement')
    )
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='advertisements',
        verbose_name=_('promotion type')
    )

    def __str__(self):
        return f'{self.advertisement.title} - {self.promotion.name}'

    class Meta:
        verbose_name = _('AdvertisementPromotion')
        verbose_name_plural = _('AdvertisementPromotions')
        db_table = 'advertisement_promotion'

    def cal_inst(self):
        time = timezone.now() - self.created_time
        if time.days >= 3:
            return False
        return True
