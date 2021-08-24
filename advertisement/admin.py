from django import forms
from django.contrib import admin

from .models import *

User = get_user_model()


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('upc', 'user', 'category', 'city', 'title', 'slug', 'status')
    list_filter = ('status', 'category')
    search_fields = ('title', 'slug')
    list_editable = ('status',)

    def save_model(self, request, obj, form, change):
        obj.set_default_fields(request.user)
        return super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=None, change=False, **kwargs)
        form.base_fields['category'] = forms.ModelChoiceField(queryset=Category.objects.exclude(parent=None))
        return form


@admin.register(AdvertisementAttribute)
class AdvertisementAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'advertisement_type', 'attribute_type')
    list_filter = ('attribute_type',)
    search_fields = ('name',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=None, change=False, **kwargs)
        form.base_fields['advertisement_type'] = forms.ModelChoiceField(
            queryset=Category.objects.exclude(parent=None).filter(children=None))
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

    def save_model(self, request, obj, form, change):
        obj.set_slug()
        return super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=None, change=False, **kwargs)
        form.base_fields['parent'] = forms.ModelChoiceField(queryset=Category.objects.exclude(parent=None))
        return form


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'state')
    search_fields = ('name', 'slug')

    def save_model(self, request, obj, form, change):
        obj.set_slug()
        return super().save_model(request, obj, form, change)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

    def save_model(self, request, obj, form, change):
        obj.set_slug()
        return super().save_model(request, obj, form, change)


@admin.register(MarK)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'advertisement')


@admin.register(AdvertisementEngagement)
class AdvertisementEngagementAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'user', 'created_time')
