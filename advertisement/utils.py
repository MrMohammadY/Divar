import json
from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import resolve_url

from advertisement.models import Advertisement, Category


def check_object_related_to_user(user, obj):
    if user != obj.user:
        raise Http404
    else:
        return True


def set_advertisement_filter(request, category_slug):
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if min_price == '':
        min_price = 0

    if max_price == '':
        max_price = 100000000000000

    instantaneous = request.GET.get('instantaneous', False)
    if category_slug:
        category = Category.objects.filter(slug=category_slug).first()
        if category is None:
            raise Http404()
    else:
        category = None
    return category, min_price, max_price, instantaneous


def add_or_create_recently_advertisements(request, response, obj):
    if request.user != obj.user:
        recently_advertisements = request.COOKIES.get('recently_advertisements', None)
        if recently_advertisements is None:
            response.set_cookie('recently_advertisements', json.dumps([obj.id]))
        else:
            recently_advertisements = json.loads(recently_advertisements)
            recently_advertisements.append(obj.id)
            response.set_cookie('recently_advertisements', json.dumps(recently_advertisements))
    return response


def object_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            obj = Advertisement.objects.get(pk=kwargs.get('pk'), slug=kwargs.get('slug'))
            if test_func(request.user, obj):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)

        return _wrapped_view

    return decorator
