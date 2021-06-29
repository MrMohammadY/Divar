from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class LoginUserForm(forms.Form):
    phone_number = forms.CharField(
        max_length=13,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'شماره تلفن'
            }
        )

    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'رمز عبور'
            }
        )

    )

    def clean(self):
        phone_number = self.cleaned_data['phone_number']
        password = self.cleaned_data['password']

        user = User.objects.filter(phone_number=phone_number).first()

        if user is not None:
            if user.check_password(password):
                self.cleaned_data['user'] = user
                return self.cleaned_data

