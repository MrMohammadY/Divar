import re

from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class LoginRegisterUserForm(forms.Form):
    phone_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'شماره تلفن'
            }
        )

    )


class ConfirmationPhoneNumberForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'کد تایید'
            }
        )
    )

