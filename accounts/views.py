from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from accounts.forms import LoginUserForm


@login_required
def profile(request):
    user = request.user
    return render(request, template_name='accounts/profile.html', context={'user': user})


class LoginUserView(FormView):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        user_q = form.cleaned_data.get('user')
        if user_q:
            user = authenticate(phone_number=user_q.phone_number, password=user_q.password)
            if user:
                login(self.request, user)
                messages.info(self.request, 'شما با موفقیت وارد حساب کاربری خود شدید', 'success')
                return super().form_valid(form)
        else:
            messages.info(self.request, 'شماره تلفن یا رمزعبور اشتباه است', 'danger')
            return super().form_valid(form)


class LogoutUserView(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(self.request)
            return redirect('advertisement:advertisement_list')
