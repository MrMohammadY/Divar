from datetime import datetime, timedelta
from random import randint

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Case, When, F, Q
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from lib.base_model import BaseModel

User = get_user_model()


class CustomAdvertisementStatusObjects(models.Manager):

    def advertisement_accepted(self):
        return super().get_queryset().filter(status=Advertisement.ACCEPTED)

    def advertisement_custom_filter(self, min_price, max_price, instantaneous, category=None):
        queryset = self.advertisement_accepted().filter(price__range=(min_price, max_price))

        if instantaneous:
            from promotion.models import Promotion
            time = timedelta(days=3)

            queryset = queryset.annotate(days=Case(When(
                promotions__promotion__name=Promotion.INSTANTANEOUS,
                then=timezone.now() - F('promotions__created_time')
            ))).filter(days__lte=time)

        if category:
            queryset = queryset.select_related('category').filter(
                Q(category__in=category.children.all()) | Q(category=category)
            )

        return queryset


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
    DRAFT = 0
    ACCEPTED = 1
    NOT_APPROVED = 2
    STATUS = (
        (DRAFT, _('draft')),
        (ACCEPTED, _('accepted')),
        (NOT_APPROVED, _('not approved')),
    )

    ad_time = models.DateTimeField(auto_now_add=True)

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
    status = models.PositiveSmallIntegerField(choices=STATUS, verbose_name=(_('status')), default=DRAFT)

    objects = models.Manager()  # The default manager.
    custom_objects = CustomAdvertisementStatusObjects()

    class Meta:
        verbose_name = _('Advertisement')
        verbose_name_plural = _('Advertisements')
        db_table = 'advertisement'
        ordering = ('-ad_time', '-created_time')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('advertisement:advertisement_detail', kwargs={'pk': self.id, 'slug': self.slug})

    def set_default_fields(self, user):
        self.user = user
        self.upc = randint(100, 10000)
        self.slug = slugify(self.title, allow_unicode=True)

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


class AdvertisementImage(BaseModel):
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


class MarK(BaseModel):
    user = models.ForeignKey(User, related_name='marks', on_delete=models.CASCADE, verbose_name=_('user'))
    advertisement = models.ForeignKey(
        Advertisement, related_name='marks', on_delete=models.CASCADE, verbose_name=_('advertisement')
    )

    class Meta:
        verbose_name = _('MarK')
        verbose_name_plural = _('MarKs')
        db_table = 'marK'


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


class AdvertisementEngagement(BaseModel):
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name='engagements',
        verbose_name=_('advertisement')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='engagements',
        verbose_name=_('user'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('AdvertisementEngagement')
        verbose_name_plural = _('AdvertisementEngagements')
        db_table = 'aAdvertisement_engagement'

    @classmethod
    def create_engagement(cls, adv, user):
        if user != adv.user:
            cls.objects.get_or_create(
                user=user if user.is_authenticated else None,
                advertisement=adv
            )
