from django.shortcuts import render, get_object_or_404

from advertisement.models import Advertisement


def advertisement_list(request):
    advertisements = Advertisement.objects.all()
    return render(request, template_name='advertisement/list.html', context={'advertisements': advertisements})


def advertisement_detail(request, uuid, slug):
    advertisement = get_object_or_404(Advertisement, uuid=uuid, slug=slug)
    return render(request, template_name='advertisement/detail.html', context={'advertisement': advertisement})


