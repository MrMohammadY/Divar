from django.db.models import Q
from django.views.generic import ListView, DetailView

from advertisement.models import Advertisement


# def advertisement_list(request):
#     advertisements = Advertisement.objects.all()
#     return render(request, template_name='advertisement/list.html', context={'advertisements': advertisements})
#
# def advertisement_detail(request, id):
#     advertisement = get_object_or_404(Advertisement, pk=id)
#     return render(request, template_name='advertisement/detail.html', context={'advertisement': advertisement})


class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'advertisement/list.html'
    context_object_name = 'advertisements'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        if self.kwargs.get('category'):

            context['advertisements'] = Advertisement.objects.filter(
                Q(category__slug=self.kwargs['category']) | Q(category__parent__slug=self.kwargs['category'])

            )

        else:
            context['advertisements'] = Advertisement.objects.all()

        return context


class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'advertisement/detail.html'
    context_object_name = 'advertisement'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
