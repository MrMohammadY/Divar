from django.urls import path
from .views import AdvertisementListView, AdvertisementDetailView

app_name = 'advertisement'

urlpatterns = [
    path('', AdvertisementListView.as_view(), name='advertisement_list'),
    path('<str:category>', AdvertisementListView.as_view(), name='advertisement_list'),
    path('detail/<int:pk>/<str:slug>', AdvertisementDetailView.as_view(), name='advertisement_detail'),
]
