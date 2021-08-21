import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods, require_GET

from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, FormView, RedirectView
from django.utils.decorators import method_decorator

from advertisement.models import *
from advertisement.forms import AdvertisementAttributeUpdateFormset, AdvertisementCreateForm, advertisement_formset, \
    AdvertisementImageCreateForm, AdvertisementImageUpdateFormset
from advertisement.utils import object_passes_test, check_object_related_to_user

User = get_user_model()


@method_decorator(require_GET, name='dispatch')
class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'advertisement/list.html'
    context_object_name = 'advertisements'

    def set_filters(self):
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        cat_slug = self.kwargs.get('category', None)

        if min_price == '':
            min_price = 0

        if max_price == '':
            max_price = 100000000000000

        instantaneous = self.request.GET.get('instantaneous', False)
        if cat_slug:
            category = Category.objects.filter(slug=cat_slug).first()
            if category is None:
                raise Http404()
        else:
            category = None
        return category, min_price, max_price, instantaneous

    def get_queryset(self):
        category, min_price, max_price, instantaneous = self.set_filters()
        query = Advertisement.custom_objects.advertisement_custom_filter(min_price, max_price, instantaneous, category)
        return query


@method_decorator(require_GET, name='dispatch')
class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'advertisement/detail.html'
    context_object_name = 'advertisement'

    def get(self, request, *args, **kwargs):
        render_to_response = super().get(request, *args, **kwargs)
        AdvertisementEngagement.create_engagement(self.object, self.request.user)
        return render_to_response

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        update_response = self.recently_advertisements(response)
        return update_response

    def recently_advertisements(self, response):
        if self.request.user != self.object.user:
            recently_advertisements = self.request.COOKIES.get('recently_advertisements', None)
            if recently_advertisements is None:
                response.set_cookie('recently_advertisements', json.dumps([self.object.id]))
            else:
                recently_advertisements = json.loads(recently_advertisements)
                recently_advertisements.append(self.object.id)
                response.set_cookie('recently_advertisements', json.dumps(recently_advertisements))
        return response


@method_decorator(login_required, name='dispatch')
@method_decorator(require_http_methods(request_method_list=('POST', 'GET')), name='dispatch')
class AdvertisementAttributeValueCreateView(FormView):
    template_name = 'advertisement/attribute.html'
    model = AdvertisementAttributeValue
    success_url = reverse_lazy('accounts:profile')

    def check_advertisement_exists(self):
        advertisement_id = self.request.session.get('advertisement_id', None)
        if advertisement_id is None:
            return redirect('advertisement:advertisement_create')
        obj = Advertisement.objects.get(pk=advertisement_id)
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.check_advertisement_exists()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.check_advertisement_exists()
        del self.request.session['advertisement_id']
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):

        if self.request.method == 'POST':
            advertisement_attribute_create_formset = advertisement_formset(extra=0)
            formset = advertisement_attribute_create_formset(self.request.POST, instance=self.object)

        else:
            attributes = AdvertisementAttribute.objects.filter(advertisement_type=self.object.type)
            advertisement_attribute_create_formset = advertisement_formset(extra=attributes.count())
            formset = advertisement_attribute_create_formset(instance=self.object)

            for index, attr in enumerate(attributes):
                from django import forms

                if attr.attribute_type == attr.FLOAT:
                    formset[index].fields['value'] = forms.FloatField()
                elif attr.attribute_type == attr.INTEGER:
                    formset[index].fields['value'] = forms.IntegerField()
                elif attr.attribute_type == attr.STRING:
                    formset[index].fields['value'] = forms.CharField()

                formset[index].fields['attribute'].initial = attr
                formset[index].fields['attribute'].widget = forms.HiddenInput()

                formset[index].fields['advertisement'].initial = self.object.id
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['image_form'] = AdvertisementImageCreateForm(self.request.POST, self.request.FILES)
        elif self.request.method == 'GET':
            context['image_form'] = AdvertisementImageCreateForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data(**self.kwargs)
        image_form = context['image_form']

        with transaction.atomic():
            obj = form.save(commit=False)
            obj.set_default_fields(self.request.user)
            obj.save()

            if image_form.is_valid():
                for img in self.request.FILES.getlist('images'):
                    AdvertisementImage.objects.create(advertisement=obj, image=img)

            self.request.session['advertisement_id'] = obj.id
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

            if self.object.images.all().exists():
                image_form = AdvertisementImageUpdateFormset(self.request.POST, self.request.FILES, instance=self.object)
            else:
                image_form = AdvertisementImageCreateForm(self.request.POST, self.request.FILES)
        else:
            from django import forms
            formset = AdvertisementAttributeUpdateFormset(instance=self.object)

            if self.object.images.all().exists():
                image_form = AdvertisementImageUpdateFormset(instance=self.object)
            else:
                image_form = AdvertisementImageCreateForm()

            for form in formset:

                if form.instance.attribute.attribute_type == AdvertisementAttribute.FLOAT:
                    form.fields['value'] = forms.FloatField()
                elif form.instance.attribute.attribute_type == AdvertisementAttribute.INTEGER:
                    form.fields['value'] = forms.IntegerField()
                elif form.instance.attribute.attribute_type == AdvertisementAttribute.STRING:
                    form.fields['value'] = forms.CharField()

                form.fields['value'].label = form.instance.attribute.name

        context['formset'] = formset
        context['image_form'] = image_form
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        image_form = context['image_form']

        with transaction.atomic():
            if formset.is_valid():
                formset.save()
            if image_form.is_valid():
                if isinstance(image_form, AdvertisementImageCreateForm):
                    for img in self.request.FILES.getlist('images'):
                        AdvertisementImage.objects.create(advertisement=self.object, image=img)
                else:
                    image_form.save()

            self.object.status = Advertisement.DRAFT
            self.object.save()
            return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(object_passes_test(check_object_related_to_user), name='dispatch', )
class AdvertisementDeleteView(DeleteView):
    model = Advertisement
    template_name = 'advertisement/delete.html'
    success_url = reverse_lazy('accounts:profile')


@method_decorator(login_required, name='dispatch')
@method_decorator(require_GET, name='dispatch')
class AdvertisementMarkView(ListView):
    model = MarK
    template_name = 'accounts/mark.html'
    context_object_name = 'marks'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


@method_decorator(require_GET, name='dispatch')
@method_decorator(login_required, name='dispatch')
class DeleteOrCreateAdvertisementMarkView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get('HTTP_REFERER')

    def get(self, request, *args, **kwargs):
        advertisement = get_object_or_404(
            Advertisement,
            id=self.kwargs.get('advertisement_id'),
            status=Advertisement.ACCEPTED
        )

        mark = self.request.user.marks.filter(advertisement=advertisement).first()
        if mark:
            mark.delete()
        else:
            self.request.user.marks.create(advertisement=advertisement)

        return super().get(request, *args, **kwargs)


@method_decorator(require_GET, name='dispatch')
class RecentlyAdvertisementView(ListView):
    model = Advertisement
    template_name = 'accounts/recently.html'
    context_object_name = 'recently_advertisements'

    def get_queryset(self):
        pk_list = self.request.COOKIES.get('recently_advertisements', None)
        if pk_list:
            pk_list = json.loads(pk_list)
            preserved = Case(*[When(pk=pk, then=index) for index, pk in enumerate(pk_list)])
            return self.model.objects.filter(id__in=pk_list).order_by(-preserved)
        return None
