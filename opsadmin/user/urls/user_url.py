from django.conf.urls import url
from .. import views

app_name = 'user'
urlpatterns = [
    url(r'login/$',views.UserLoginView.as_view(),name='login'),
    url(r'register/$',views.UserRegisterView.as_view(),name='register'),
    url(r'system/(?P<pk>[0-9]+)/update/$',views.system_user_update.as_view(),name='system_user_update'),
    url(r'(?P<pk>[0-9]+)/update/$',views.user_update.as_view(),name='update'),
    url(r'logout/$',views.user_logout,name='logout'),
    url(r'head/$',views.head_pic_set.as_view(),name='head_set'),
    url(r'head/update/$',views.head_pic_update.as_view(),name='head_update'),
    url(r'info/$',views.myuser_info.as_view(),name='info'),
    url(r'system/create/$',views.create_system_user.as_view(),name='system_user_create'),
    url(r'system/list/$',views.system_user_list.as_view(),name='system_user_list'),
    url(r'permission/admin/authorized/(?P<name>\w+)/$',views.AdminAuthorized.as_view()),

]