from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
@login_required
def profile(request):
    user = request.user
    return render(request, template_name='accounts/profile.html', context={'user': user})
