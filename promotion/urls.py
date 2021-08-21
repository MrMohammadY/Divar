from django.urls import path
from .views import AdvertisementPromotionView

app_name = 'promotion'

urlpatterns = [
    path('<int:advertisement_id>', AdvertisementPromotionView.as_view(), name='advertisement-promotion'),
]
