import json
import random

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods, require_GET

from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, FormView, RedirectView
from django.utils.decorators import method_decorator

from advertisement.models import *
from advertisement.forms import AdvertisementAttributeUpdateFormset, AdvertisementCreateForm, set_extra_formset
from advertisement.utils import object_passes_test, check_object_related_to_user

User = get_user_model()


@method_decorator(require_GET, name='dispatch')
class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'advertisement/list.html'
    context_object_name = 'advertisements'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['categories'] = Category.objects.filter(parent=None)

        min_price = self.request.GET.get('min_price', None)
        max_price = self.request.GET.get('max_price', None)

        if min_price == '' or min_price is None:
            min_price = 0

        if max_price == '' or max_price is None:
            max_price = 100000000000000

        if self.kwargs.get('category'):
            category = Category.objects.filter(slug=self.kwargs.get('category')).first()

            if category is None:
                raise Http404()

            if category.parent is None:
                context['advertisements'] = Advertisement.status_objects.accepted_advertisement().filter(
                    category__in=category.children.all(),
                    price__range=(min_price, max_price)
                )
            else:
                context['advertisements'] = Advertisement.status_objects.accepted_advertisement().filter(
                    category=category,
                    price__range=(min_price, max_price)
                )

        else:
            context['advertisements'] = Advertisement.status_objects.accepted_advertisement().filter(
                price__range=(min_price, max_price)
            )

        return context


@method_decorator(require_GET, name='dispatch')
class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'advertisement/detail.html'
    context_object_name = 'advertisement'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        recently_advertisements = self.request.COOKIES.get('recently_advertisements', None)
        if recently_advertisements is None:
            response.set_cookie('recently_advertisements', json.dumps([self.object.id]))
        else:
            recently_advertisements = json.loads(recently_advertisements)
            print(recently_advertisements)
            recently_advertisements.append(self.object.id)
            response.set_cookie('recently_advertisements', json.dumps(recently_advertisements))

        return response


@method_decorator(login_required, name='dispatch')
@method_decorator(require_http_methods(request_method_list=('POST', 'GET')), name='dispatch')
class AdvertisementAttributeValueCreateView(FormView):
    template_name = 'advertisement/attribute.html'
    model = AdvertisementAttributeValue
    success_url = reverse_lazy('accounts:profile')

    def get(self, request, *args, **kwargs):
        advertisement_id = self.request.session.get('advertisement_id', None)
        if advertisement_id is None:
            return redirect('advertisement:advertisement_create')
        self.object = Advertisement.objects.get(pk=advertisement_id)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        advertisement_id = self.request.session.get('advertisement_id', None)
        if advertisement_id is None:
            return redirect('advertisement:advertisement_create')

        self.object = Advertisement.objects.get(pk=advertisement_id)
        del self.request.session['advertisement_id']
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        attributes = AdvertisementAttribute.objects.filter(advertisement_type=self.object.type)

        if self.request.method == 'POST':
            advertisement_attribute_create_formset = set_extra_formset(extra=0)
            formset = advertisement_attribute_create_formset(self.request.POST, instance=self.object)

        else:
            advertisement_attribute_create_formset = set_extra_formset(extra=attributes.count())
            formset = advertisement_attribute_create_formset(instance=self.object)

            for index, attr in enumerate(attributes):
                from django import forms
                formset[index].fields['attribute'].initial = attr
                formset[index].fields['advertisement'].initial = self.object.id
                formset[index].fields['attribute'].widget = forms.HiddenInput()
                formset[index].fields['advertisement'].widget = forms.HiddenInput()
                formset[index].fields['value'].label = attr.name

        return formset

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class AdvertisementCreateView(CreateView):
    model = Advertisement
    form_class = AdvertisementCreateForm
    template_name = 'advertisement/create.html'
    success_url = reverse_lazy('advertisement:advertisement_attribute_create')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.upc = random.randint(1000, 10000)
            self.object.slug = slugify(self.object.title, allow_unicode=True)
            self.object.save()
            self.request.session['advertisement_id'] = self.object.id
            return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(object_passes_test(check_object_related_to_user), name='dispatch')
class AdvertisementUpdateView(UpdateView):
    model = Advertisement
    template_name = 'advertisement/update.html'
    fields = ('title', 'description', 'price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            formset = AdvertisementAttributeUpdateFormset(self.request.POST, instance=self.object)
        else:
            formset = AdvertisementAttributeUpdateFormset(instance=self.object)
            for form in formset:
                form.fields['value'].label = form.instance.attribute.name

        context['formset'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(object_passes_test(check_object_related_to_user), name='dispatch', )
class AdvertisementDeleteView(DeleteView):
    model = Advertisement
    success_url = reverse_lazy('accounts:profile')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'advertisement/delete.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(require_GET, name='dispatch')
class AdvertisementMarkView(ListView):
    model = MarK
    template_name = 'accounts/mark.html'
    context_object_name = 'marks'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


@method_decorator(require_GET, name='dispatch')
class DeleteOrCreateAdvertisementMarkView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get('HTTP_REFERER')

    def get(self, request, *args, **kwargs):
        advertisement = get_object_or_404(Advertisement, id=self.kwargs.get('advertisement_id'))

        if advertisement.status == Advertisement.ACCEPTED:
            mark = self.request.user.marks.filter(advertisement=advertisement).first()
            if mark is None:
                self.request.user.marks.create(advertisement=advertisement)
            else:
                mark.delete()

            return super().get(request, *args, **kwargs)

        raise Http404


@method_decorator(require_GET, name='dispatch')
class RecentlyAdvertisementView(ListView):
    model = Advertisement
    template_name = 'accounts/recently.html'
    context_object_name = 'recently_advertisements'

    def get_queryset(self):
        id_set = self.request.COOKIES.get('recently_advertisements', None)
        if id_set is not None:
            return self.model.objects.filter(id__in=set(json.loads(id_set)))
        return None
