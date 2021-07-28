from django.contrib.auth.decorators import login_required
from django.urls import path

from advertisement.views import AdvertisementListView, AdvertisementDetailView, AdvertisementUpdateView, \
    AdvertisementDeleteView, AdvertisementCreateView, AdvertisementAttributeValueCreateView,\
    DeleteOrCreateAdvertisementMarkView, AdvertisementMarkView

app_name = 'advertisement'

urlpatterns = [
    path('', AdvertisementListView.as_view(), name='advertisement_list'),
    path('<str:category>', AdvertisementListView.as_view(), name='advertisement_list'),
    path('detail/<int:pk>/<str:slug>', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    path('create/', AdvertisementCreateView.as_view(), name='advertisement_create'),
    path('create/attribute/', AdvertisementAttributeValueCreateView.as_view(), name='advertisement_attribute_create'),
    path('detail/<int:pk>/<str:slug>/update', AdvertisementUpdateView.as_view(), name='advertisement_update'),
    path('<int:pk>/<str:slug>/delete/confirm', AdvertisementDeleteView.as_view(), name='advertisement_delete_confirm'),
    path('mark/<int:advertisement_id>', DeleteOrCreateAdvertisementMarkView.as_view(), name='mark_advertisement'),
]
