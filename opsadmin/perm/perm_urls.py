from django.conf.urls import url
from .views import create_perm,list_perm,perm_asset_host_connect_list,delete_perm

app_name = 'perm'

urlpatterns = [
    url(r'^create/$',create_perm.as_view(),name='perm_create'),
    url(r'^list/$',list_perm.as_view(),name='perm_list'),
    url(r'^(?P<pk>[0-9]+)/delete/$',delete_perm.as_view(),name='perm_delete'),
    url(r'^(?P<name>\w+)/connect/list/$',perm_asset_host_connect_list.as_view(),name='perm_asset_host_connect_list'),
]