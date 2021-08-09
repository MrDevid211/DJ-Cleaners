from django.urls import path, re_path

from .views import CleanerList, CleanerDetail, CleanerCreation, CleanerUpdate, CleanerDelete


urlpatterns = [

    re_path(r'^$', CleanerList.as_view(), name='list'),
    re_path(r'^(?P<pk>\d+)$', CleanerDetail.as_view(), name='detail'),
    re_path(r'^new$', CleanerCreation.as_view(), name='new'),
    re_path(r'^edit/(?P<pk>\d+)$', CleanerUpdate.as_view(), name='edit'),
    re_path(r'^delete/(?P<pk>\d+)$', CleanerDelete.as_view(), name='delete'),

]