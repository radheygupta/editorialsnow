from django.conf.urls import url
from . import views

app_name = 'editorials'

urlpatterns = [
    url(r'^show/(?P<edt_id>\d+)/', views.display, name='display-url'),
    url(r'^page/(?P<page>\d+)/', views.index, name='index-url'),
    url(r'^$', views.index, name='index-url-withoutpage'),
    #ajax
    url(r'^ajaxsignup', views.ajaxsignup, name='usersignup'),
    url(r'^ajaxlogin', views.ajaxlogin, name='userlogin'),
    url(r'^userlogout', views.userlogout, name='userlogout'),
    url(r'updateprofile',views.update_profile, name='updateprofile'),
    url(r'^userlogin', views.userlogin, name='userlogin'),
    url(r'^userregistration', views.userregistration, name='userregistration'),
]
