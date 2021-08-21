from django import forms

from promotion.models import AdvertisementPromotion


class AdvertisementPromotionForm(forms.ModelForm):
    class Meta:
        model = AdvertisementPromotion
        fields = ('promotion',)
