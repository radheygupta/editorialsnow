from django.conf.urls import url
from . import views

app_name = 'editorials'

urlpatterns = [
    url(r'^show/(?P<edt_id>\d+)/', views.display, name='display-url'),

    url(r'^page/(?P<page>\d+)/', views.index, name='index-url'),
    url(r'^$', views.index, name='index-url-withoutpage'),
]
