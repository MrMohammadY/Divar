from django.urls import path
from .views import advertisement_list, advertisement_detail

app_name = 'advertisement'

urlpatterns = [
    path('', advertisement_list, name='advertisement_list'),
    path('detail/<int:uuid>/<slug:slug>/', advertisement_detail, name='advertisement_detail'),
]
