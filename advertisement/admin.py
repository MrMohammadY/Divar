from django.contrib import admin

from .models import Advertisement, AdvertisementType, AdvertisementAttribute, AdvertisementAttributeValue, \
    AdvertisementImages, Category, City, State, MarK


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('upc', 'type', 'user', 'category', 'city', 'title', 'slug', 'status')
    list_filter = ('type', 'status')
    search_fields = ('title', 'slug')
    list_editable = ('status',)


@admin.register(AdvertisementType)
class AdvertisementTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(AdvertisementAttribute)
class AdvertisementAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'advertisement_type', 'attribute_type')
    list_filter = ('attribute_type',)
    search_fields = ('name',)


@admin.register(AdvertisementAttributeValue)
class AdvertisementAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'attribute', 'value')
    search_fields = ('value',)


@admin.register(AdvertisementImages)
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
