from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.base_model import BaseModel
from promotion.models import Promotion

User = get_user_model()


class Transaction(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name=_('user')
    )

    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name=_('promotion')
    )
    price = models.IntegerField()

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        db_table = 'transaction'


class UserPurchase(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='purchases',
        verbose_name=_('user')
    )

    balance = models.IntegerField()

    class Meta:
        verbose_name = _('UserPurchase')
        verbose_name_plural = _('UserPurchases')
        db_table = 'user_purchase'
