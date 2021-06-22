from django.urls import path
from .views import advertisement_list

app_name = 'advertisement'

urlpatterns = [
    path('', advertisement_list, name='advertisement_list'),
]
