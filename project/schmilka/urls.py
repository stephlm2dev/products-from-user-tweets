from django.conf.urls import url

from . import views

urlpatterns = [
    # URL: /
    url(r'^$', views.index, name='index'),

    # URL: /ajaxTwitterUser
    url(r'^ajaxTwitterUser$', views.ajaxTwitterUser, name='ajaxTwitterUser'),

    # URL: /process
    url(r'^process$', views.process, name='process'),

    # URL: /products
    url(r'^products/(?P<username>[A-Za-z0-9_]+)$', views.results, name='results'),

    

]
