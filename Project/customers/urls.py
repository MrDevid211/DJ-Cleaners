from django.conf.urls import url
from django.urls import path, re_path

from . import views
from .views import CustomerList, CustomerDetail, customer_creation, CustomerUpdate, CustomerDelete


urlpatterns = [

    url(r'^$', CustomerList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)$', CustomerDetail.as_view(), name='detail'),
    re_path('new', views.customer_creation),
    url(r'^edit/(?P<pk>\d+)$', CustomerUpdate.as_view(), name='edit'),
    url(r'^delete/(?P<pk>\d+)$', CustomerDelete.as_view(), name='delete'),

]