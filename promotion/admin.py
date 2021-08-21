from django.contrib import admin
from .models import *


@admin.register(AdvertisementPromotion)
class AdvertisementPromotionAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'promotion', 'created_time')
    list_filter = ('promotion',)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
