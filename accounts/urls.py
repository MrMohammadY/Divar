from django.contrib.auth.decorators import login_required
from django.urls import path

from advertisement.views import AdvertisementMarkView, RecentlyAdvertisementView
from .views import ProfileView, LoginRegisterUserView, LogoutUserView, ConfirmationPhoneNumberView

app_name = 'accounts'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginRegisterUserView.as_view(), name='login-register'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', LoginRegisterUserView.as_view(), name='login-register'),
    path('confirmation/', ConfirmationPhoneNumberView.as_view(), name='confirmation'),
    path('mark/', AdvertisementMarkView.as_view(), name='show-advertisement-mark'),
    path('recently/', RecentlyAdvertisementView.as_view(), name='show-recently-advertisements'),

]
