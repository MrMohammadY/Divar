from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.base_model import BaseModel

User = get_user_model()


class AdvertisementType(BaseModel):
    title = models.CharField(max_length=30, verbose_name=_('title'), unique=True)

    class Meta:
        verbose_name = 'Advertisement Type'
        verbose_name_plural = 'Advertisement Types'
        db_table = 'advertisement_type'


class AdvertisementAttribute(BaseModel):
    INTEGER = 1
    FLOAT = 2
    STRING = 3

    STATUS = (
        (INTEGER, _('Integer')),
        (FLOAT, _('Float')),
        (STRING, _('String')),
    )
    name = models.CharField(max_length=32, verbose_name=_('name'), unique=True)
    advertisement_type = models.ForeignKey(AdvertisementType, related_name='attributes', on_delete=models.CASCADE)
    attribute_type = models.PositiveSmallIntegerField(verbose_name=_('attribute type'), choices=STATUS)

    class Meta:
        verbose_name = _('Advertisement Attribute')
        verbose_name_plural = _('Advertisement Attributes')
        db_table = 'advertisement_attribute'


class AdvertisementAttributeValue(BaseModel):
    advertisement = models.ForeignKey('Advertisement', related_name='values', on_delete=models.CASCADE)
    attribute = models.ForeignKey(AdvertisementAttribute, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=64)

    class Meta:
        verbose_name = _('Advertisement Attribute Value')
        verbose_name_plural = _('Advertisement Attribute Values')
        db_table = 'advertisement_attribute_value'


class Advertisement(BaseModel):
    uuid = models.BigIntegerField(unique=True)
    type = models.ForeignKey(
        AdvertisementType,
        related_name='advertisements',
        on_delete=models.PROTECT,
        verbose_name=_('type')
    )

    user = models.ForeignKey(
        User,
        related_name='advertisements',
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )

    category = models.ForeignKey(
        'Category',
        related_name='advertisements',
        on_delete=models.PROTECT,
        verbose_name=_('category')
    )

    city = models.ForeignKey(
        'City',
        related_name='advertisements',
        on_delete=models.PROTECT,
        verbose_name=_('city')
    )

    title = models.CharField(max_length=64, verbose_name=_('title'))
    description = models.CharField(max_length=180, verbose_name=_('description'))
    price = models.BigIntegerField(verbose_name=_('price'))
    slug = models.SlugField(verbose_name=_('slug'))
    is_agreement = models.BooleanField(verbose_name=_('is agreement'), default=False)
    is_available = models.BigIntegerField(verbose_name=_('is available'), default=False)

    class Meta:
        verbose_name = _('Advertisement')
        verbose_name_plural = _('Advertisements')
        db_table = 'advertisement'
        ordering = ('created_time', )


class AdvertisementImages(BaseModel):
    advertisement = models.ForeignKey(
        Advertisement,
        related_name='images',
        on_delete=models.CASCADE,
        verbose_name=_('advertisement')
    )
    image = models.ImageField(
        upload_to='advertisements/images/',
        verbose_name='images',
        blank=True,
        null=True,
    )


class Category(BaseModel):
    name = models.CharField(max_length=30, verbose_name=_('name'))
    slug = models.SlugField(verbose_name=_('slug'))
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        db_table = 'category'


class State(BaseModel):
    name = models.CharField(max_length=20, verbose_name=_('name'))
    slug = models.SlugField(verbose_name=_('slug'))

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        db_table = 'state'


class City(BaseModel):
    name = models.CharField(max_length=40, verbose_name=_('name'))
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        db_table = 'city'
