from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView
from django.http import Http404

from advertisement.models import Advertisement
from promotion.forms import AdvertisementPromotionForm
from promotion.models import Promotion
from transaction.models import Transaction


class AdvertisementPromotionView(FormView):
    form_class = AdvertisementPromotionForm
    template_name = 'promotion.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs['advertisement_id'])
        ladder_condition = advertisement.promotions.filter(promotion__name=Promotion.LADDER).exists()
        ins_condition = advertisement.promotions.filter(promotion__name=Promotion.INSTANTANEOUS).last()

        with transaction.atomic():
            obj = form.save(commit=False)

            if ins_condition is not None and obj.promotion.name == Promotion.INSTANTANEOUS and ins_condition.cal_inst():
                raise Http404

            elif obj.promotion.name == Promotion.LADDER and ladder_condition:
                raise Http404

            else:

                Transaction.objects.create(user=self.request.user, promotion=obj.promotion, price=obj.promotion.price)
                obj.advertisement = advertisement
                obj.save()

                if obj.promotion.name == Promotion.LADDER:
                    advertisement.ad_time = timezone.now()
                    advertisement.save()

                return super().form_valid(form)
