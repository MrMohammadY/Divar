from django.urls import path
from .views import profile, LoginUserView, LogoutUserView

app_name = 'accounts'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]