from django.conf.urls import url
from .views import SessionActionList,SessionActionDetail,SessionActionDelete
app_name = 'log'

urlpatterns = [
    url(r'^session/action/list/$',SessionActionList.as_view(),name='session_action_list'),
    url(r'^session/action/(?P<pk>[0-9]+)/replay/$',SessionActionDetail.as_view(),name='session_action_replay'),
    url(r'^session/action/(?P<pk>[0-9]+)/delete/$',SessionActionDelete.as_view(),name='session_action_delete'),
]