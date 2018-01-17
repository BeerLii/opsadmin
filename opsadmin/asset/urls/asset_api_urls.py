from django.conf.urls import url,include

from .. import views




urlpatterns = [
    url(r'^collect/$',views.collect_asset.as_view()),
    url(r'^delete/(?P<pk>\d+)$',views.delete_asset.as_view()),
    url(r'^group/delete/(?P<pk>\d+)$',views.delete_asset_group.as_view()),
]