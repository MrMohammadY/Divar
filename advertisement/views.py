from django.shortcuts import render

from advertisement.models import Advertisement


def advertisement_list(request):
    advertisements = Advertisement.objects.all()
    return render(request, template_name='advertisement/list.html', context={'advertisements': advertisements})
