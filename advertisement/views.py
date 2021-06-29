from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.http import Http404

from advertisement.models import Advertisement, Category


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
            category = Category.objects.filter(
                Q(slug=self.kwargs['category']) | Q(parent__slug=self.kwargs['category'])
            ).first()

            if category is None:
                raise Http404()

            context['advertisements'] = Advertisement.objects.filter(
                Q(category__slug=category.slug) | Q(category__parent__slug=category.slug)
            )

        else:
            context['advertisements'] = Advertisement.objects.all()

        context['categories'] = Category.objects.filter(parent=None)

        return context


class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'advertisement/detail.html'
    context_object_name = 'advertisement'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
