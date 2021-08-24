import random

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View, TemplateView

from accounts.forms import LoginRegisterUserForm, ConfirmationPhoneNumberForm

from datetime import datetime

from accounts.utils import check_expire_time, set_phone_number_session

User = get_user_model()


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advertisements'] = self.request.user.advertisements.all()
        return context


class LogoutUserView(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(self.request)
            return redirect('advertisement:advertisement_list')
        else:
            return redirect('advertisement:advertisement_list')


class LoginRegisterUserView(FormView):
    form_class = LoginRegisterUserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:confirmation')

    def form_valid(self, form):
        set_phone_number_session(self.request, form.cleaned_data['phone_number'])
        return super().form_valid(form)


class ConfirmationPhoneNumberView(FormView):
    form_class = ConfirmationPhoneNumberForm
    template_name = 'accounts/confirmation.html'
    success_url = reverse_lazy('accounts:profile')

    def delete_code(self):
        del self.request.session['code']

    def dispatch(self, request, *args, **kwargs):
        check_expire_time(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        phone_number = '98' + self.request.session['phone_number']
        form_code = int(form.cleaned_data['code'])
        session_code = self.request.session.get('code', None)

        if session_code:

            if form_code == session_code:
                user, create = User.objects.get_or_create(phone_number=phone_number)
                self.delete_code()
                if create:
                    password = User.objects.make_random_password()
                    user.set_password(password)
                    user.save()

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
        else:
            messages.info(self.request, 'کد تایید اشتباه است! لطفا دوباره تلاش کنید!', 'danger')
            return redirect('accounts:login-register')
