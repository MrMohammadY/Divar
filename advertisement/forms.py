from django.forms.models import inlineformset_factory
from advertisement.models import Advertisement, AdvertisementAttributeValue, AdvertisementImage, Category
from django import forms

AdvertisementAttributeUpdateFormset = inlineformset_factory(
    Advertisement,
    AdvertisementAttributeValue,
    fields=('value',),
    extra=0,
    can_delete=False,
)


def advertisement_formset(extra):
    return inlineformset_factory(
        Advertisement,
        AdvertisementAttributeValue,
        fields=('value', 'attribute', 'advertisement'),
        extra=extra,
        can_delete=False,
    )


class AdvertisementCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.exclude(parent=None).filter(children=None))

    class Meta:
        model = Advertisement
        fields = ('category', 'city', 'title', 'description', 'price', 'is_agreement')


class AdvertisementImageCreateForm(forms.Form):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


AdvertisementImageUpdateFormset = inlineformset_factory(
    Advertisement,
    AdvertisementImage,
    fields=('image',),
    extra=0,
    can_delete=True
)
