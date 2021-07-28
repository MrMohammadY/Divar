from django.forms.models import inlineformset_factory, formset_factory
from advertisement.models import Advertisement, AdvertisementAttributeValue, AdvertisementType, AdvertisementAttribute
from django import forms

AdvertisementAttributeUpdateFormset = inlineformset_factory(
    Advertisement,
    AdvertisementAttributeValue,
    fields=('value',),
    extra=0,
    can_delete=False,
)


def set_extra_formset(extra):
    return inlineformset_factory(
        Advertisement,
        AdvertisementAttributeValue,
        fields=('value', 'attribute', 'advertisement'),
        extra=extra,
        can_delete=False,
    )


class AdvertisementAttributeCreateForm(forms.Form):
    value = forms.CharField()
    attribute = forms.ModelChoiceField(queryset=AdvertisementAttribute.objects.all(), widget=forms.HiddenInput)
    advertisement = forms.ModelChoiceField(queryset=Advertisement.objects.all(), widget=forms.HiddenInput)


class AdvertisementAttributeValueCreateForm(forms.ModelForm):
    class Meta:
        model = AdvertisementAttributeValue
        fields = ('value',)


class AdvertisementCreateForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('type', 'category', 'city', 'title', 'description', 'price', 'is_agreement')
