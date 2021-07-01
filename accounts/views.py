import random

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View, TemplateView

from accounts.forms import LoginRegisterUserForm, ConfirmationPhoneNumberForm

User = get_user_model()


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['advertisements'] = request.user.advertisements.all()
        return self.render_to_response(context)


class LoginRegisterUserView(FormView):
    form_class = LoginRegisterUserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:confirmation')

    def form_valid(self, form):
        self.request.session['phone_number'] = form.cleaned_data['phone_number']
        self.request.session['code'] = random.randint(1000, 9999)
        print(self.request.session['code'])
        return super().form_valid(form)


class LogoutUserView(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(self.request)
            return redirect('advertisement:advertisement_list')
        else:
            return redirect('advertisement:advertisement_list')


class ConfirmationPhoneNumberView(FormView):
    form_class = ConfirmationPhoneNumberForm
    template_name = 'accounts/confirmation.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        phone_code = '98'

        if int(form.cleaned_data['code']) == self.request.session['code']:
            phone_number = phone_code + self.request.session['phone_number']

            user, create = User.objects.get_or_create(phone_number=phone_number)

            user = authenticate(phone_number=user.phone_number)

            if user:
                login(self.request, user)
                messages.info(self.request, 'شما با موفقیت وارد حساب کاربری خود شدید', 'success')
                return super().form_valid(form)
            else:
                return super().form_valid(form)
        else:
            messages.info(self.request, 'کد تایید اشتباه است!', 'danger')
            return redirect('accounts:confirmation')
