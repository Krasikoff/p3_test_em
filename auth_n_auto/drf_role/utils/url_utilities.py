from django.conf import settings
from django.urls import URLResolver, URLPattern
from django.urls.base import resolve, reverse_lazy

URL_NAMES = []


def get_view_by_url(url_name=None):
    """
    **view generator**
    :param url_name: get url_name as string
    :return: view function (Though it is class or something)
    """
    if not url_name:
        return None
    url = reverse_lazy(url_name)
    resolver_match = resolve(url)
    return resolver_match.func


def get_all_url_names(urlpatterns):
    """
    :param urlpatterns: django url formatted patterns
    :return: global var URL_NAMES
    """
    for pattern in urlpatterns:
        if isinstance(pattern, URLResolver):
            if pattern.namespace is not None:
                continue
            get_all_url_names(pattern.url_patterns)
        elif isinstance(pattern, URLPattern):
            url_name = pattern.name
            if url_name:
                URL_NAMES.append(url_name)
    return URL_NAMES


def get_urls(*args, **kwargs):
    """
    :param args: expecting any tuple (still not implemented)
    :param kwargs: expecting any dictionary like object (still not implemented)
    :return: a function call as a list
    """
    global URL_NAMES
    URL_NAMES = []
    root_urlconf = __import__(settings.ROOT_URLCONF)
    all_urlpatterns = root_urlconf.urls.urlpatterns
    get_all_url_names(all_urlpatterns)
    return URL_NAMES
