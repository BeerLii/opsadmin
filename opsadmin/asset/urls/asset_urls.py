from django.conf.urls import url,include
from .. import views

app_name = 'asset'


urlpatterns = [
    url(r'^create/$',views.Asset_Create.as_view(),name='asset_create'),
    url(r'^group/(?P<pk>[0-9]+)/delete/$',views.asset_group_delete.as_view(),name='asset_group_delete'),
    url(r'group/(?P<pk>[0-9]+)/detail/$',views.asset_group_detail.as_view(),name='asset_group_detail'),
    url(r'^(?P<pk>[0-9]+)/delete/$',views.Asset_Delete.as_view(),name='asset_delete'),
    url(r'^list/$',views.Asset_List.as_view(),name='asset_list'),
    url(r'^detail/$',views.Asset_Detail.as_view(),name='asset_detail'),
    url(r'^group/create/$',views.asset_group_create.as_view(),name='asset_group_create'),
    url(r'^group/list/$',views.asset_group_list.as_view(),name='asset_group_list'),
    url(r'^(?P<perm_name>\w+)/(?P<asset_name>\w+)/(?P<system_user>\w+)/connect/$',views.Asset_Connect.as_view(),name='asset_connect'),

]