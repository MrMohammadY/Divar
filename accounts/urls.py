from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import ProfileView, LoginRegisterUserView, LogoutUserView, ConfirmationPhoneNumberView

app_name = 'accounts'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginRegisterUserView.as_view(), name='login-register'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', LoginRegisterUserView.as_view(), name='login-register'),
    path('confirmation/', ConfirmationPhoneNumberView.as_view(), name='confirmation'),
]
