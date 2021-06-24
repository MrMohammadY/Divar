from datetime import datetime

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

    def __str__(self):
        return self.title


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

    def __str__(self):
        return f'{self.advertisement_type}: {self.name}'


class AdvertisementAttributeValue(BaseModel):
    advertisement = models.ForeignKey('Advertisement', related_name='values', on_delete=models.CASCADE)
    attribute = models.ForeignKey(AdvertisementAttribute, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=64)

    class Meta:
        verbose_name = _('Advertisement Attribute Value')
        verbose_name_plural = _('Advertisement Attribute Values')
        db_table = 'advertisement_attribute_value'

    def __str__(self):
        return f'{self.advertisement}({self.attribute}): {self.value}'


class Advertisement(BaseModel):
    upc = models.BigIntegerField(unique=True)
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
    slug = models.SlugField(verbose_name=_('slug'), allow_unicode=True)
    is_agreement = models.BooleanField(verbose_name=_('is agreement'), default=False)
    is_available = models.BooleanField(verbose_name=_('is available'), default=False)

    class Meta:
        verbose_name = _('Advertisement')
        verbose_name_plural = _('Advertisements')
        db_table = 'advertisement'
        ordering = ('created_time',)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('advertisement:advertisement_detail', kwargs={'pk': self.id, 'slug': self.slug})

    def date_time_advertisement(self):
        created_time = datetime.strptime(self.created_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        current_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        different_time = current_time - created_time

        if different_time.days == 0:
            if different_time.seconds // 3600 == 0:
                return 'لحظاتی پیش در'
            else:
                return f' {different_time.seconds // 3600} ساعت پیش در '
        else:
            return f' {different_time.days} روز پیش در '

    def __str__(self):
        return self.title


class AdvertisementImages(BaseModel):
    advertisement = models.ForeignKey(
        Advertisement,
        related_name='images',
        on_delete=models.CASCADE,
        verbose_name=_('advertisement')
    )
    image = models.ImageField(
        upload_to='advertisements/images/',
        verbose_name=_('image'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Advertisement Image')
        verbose_name_plural = _('Advertisement Images')
        db_table = 'advertisement_image'


class Category(BaseModel):
    name = models.CharField(max_length=30, verbose_name=_('name'), unique=True)
    slug = models.SlugField(verbose_name=_('slug'), allow_unicode=True, unique=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        db_table = 'category'

    def __str__(self):
        return self.name


class State(BaseModel):
    name = models.CharField(max_length=20, verbose_name=_('name'), unique=True)
    slug = models.SlugField(verbose_name=_('slug'), allow_unicode=True, unique=True)

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        db_table = 'state'

    def __str__(self):
        return self.name


class City(BaseModel):
    name = models.CharField(max_length=40, verbose_name=_('name'), unique=True)
    slug = models.SlugField(verbose_name=_('slug'), allow_unicode=True, unique=True)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        db_table = 'city'

    def __str__(self):
        return self.name
