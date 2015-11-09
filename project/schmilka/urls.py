from django.conf.urls import url

from . import views

urlpatterns = [
    # URL: /
    url(r'^$', views.index, name='index'),
    # URL: /
    url(r'^(?P<username>[a-z]+)/$', views.results, name='results'),
]
