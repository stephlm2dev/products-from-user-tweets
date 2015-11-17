from django.conf.urls import url

from . import views

urlpatterns = [
    # URL: /
    url(r'^$', views.index, name='index'),

    # URL: /handleData
    url(r'^process$', views.process, name='process'),

    # URL: /products
    url(r'^products/(?P<username>[A-Za-z0-9_]+)$', views.results, name='results'),

    # url(r'^products/(?P<username>[a-z]+)/$', views.results, name='results'),

]
