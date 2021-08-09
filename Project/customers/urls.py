from django.conf.urls import url

from .views import CustomerList, CustomerDetail, CustomerCreation, CustomerUpdate, CustomerDelete


urlpatterns = [

    url(r'^$', CustomerList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)$', CustomerDetail.as_view(), name='detail'),
    url(r'^new$', CustomerCreation.as_view(), name='new'),
    url(r'^edit/(?P<pk>\d+)$', CustomerUpdate.as_view(), name='edit'),
    url(r'^delete/(?P<pk>\d+)$', CustomerDelete.as_view(), name='delete'),

]