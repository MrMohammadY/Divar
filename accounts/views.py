import random

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View, TemplateView

from accounts.forms import LoginRegisterUserForm, ConfirmationPhoneNumberForm

from datetime import datetime, timedelta

User = get_user_model()


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['advertisements'] = request.user.advertisements.all()
        return self.render_to_response(context)


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
        self.request.session['phone_number'] = form.cleaned_data['phone_number']
        self.request.session['code'] = random.randint(1000, 9999)
        self.request.session['expire_code_time'] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print(self.request.session['code'])
        print(self.request.session['expire_code_time'])

        return super().form_valid(form)


class ConfirmationPhoneNumberView(FormView):
    form_class = ConfirmationPhoneNumberForm
    template_name = 'accounts/confirmation.html'
    success_url = reverse_lazy('accounts:profile')

    def delete_code_expire_time(self):
        try:
            expire_time = datetime.strptime(self.request.session['expire_code_time'], '%Y-%m-%d %H:%M:%S')
        except KeyError:
            expire_time = None

        if expire_time:
            now = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            if (now - expire_time) > timedelta(minutes=2):
                del self.request.session['code']
                del self.request.session['expire_code_time']

    def get(self, request, *args, **kwargs):
        self.delete_code_expire_time()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.delete_code_expire_time()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        phone_code = '98'

        if self.request.session.get('code'):

            if int(form.cleaned_data['code']) == self.request.session['code']:

                phone_number = phone_code + self.request.session['phone_number']
                user, create = User.objects.get_or_create(phone_number=phone_number, )

                if create:
                    password = User.objects.make_random_password()
                    user.set_password(password)
                    user.save()

                user = authenticate(phone_number=user.phone_number)

                if user:
                    login(self.request, user)
                    messages.info(self.request, 'شما با موفقیت وارد حساب کاربری خود شدید', 'success')
                    del self.request.session['code']
                    return super().form_valid(form)

                else:
                    del self.request.session['code']
                    return super().form_valid(form)

            else:
                messages.info(self.request, 'کد تایید اشتباه است!', 'danger')
                return redirect('accounts:confirmation')
        else:
            messages.info(self.request, 'کد تایید اشتباه است! لطفا دوباره تلاش کنید!', 'danger')
            return redirect('accounts:login-register')
