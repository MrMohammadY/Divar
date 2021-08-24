from django import forms
from django.contrib import admin

from .models import *


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('upc', 'user', 'category', 'city', 'title', 'slug', 'status')
    list_filter = ('status', 'category')
    search_fields = ('title', 'slug')
    list_editable = ('status',)


@admin.register(AdvertisementAttribute)
class AdvertisementAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'advertisement_type', 'attribute_type')
    list_filter = ('attribute_type',)
    search_fields = ('name',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=None, change=False, **kwargs)
        form.base_fields['advertisement_type'] = forms.ModelChoiceField(queryset=Category.objects.exclude(parent=None))
        return form


@admin.register(AdvertisementAttributeValue)
class AdvertisementAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'attribute', 'value')
    search_fields = ('value',)


@admin.register(AdvertisementImage)
class AdvertisementImagesAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'image')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    list_filter = ('parent',)
    search_fields = ('name', 'slug')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'state')
    search_fields = ('name', 'slug')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(MarK)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'advertisement')


@admin.register(AdvertisementEngagement)
class AdvertisementEngagementAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'user', 'created_time')
