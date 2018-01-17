"""opsadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from user.urls import user_url
from asset.urls import asset_urls,asset_api_urls
from .dashboard import dashboard,testview
from rest_framework_jwt.views import obtain_jwt_token
from perm import perm_urls
from log import log_url


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^opsadmin/$',dashboard.as_view(),name='dashboard'),
    url(r'^opsadmin/user/',include(user_url)),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^opsadmin/asset/',include(asset_urls)),
    url(r'^api/asset/',include(asset_api_urls)),
    url(r'^opsadmin/perm/',include(perm_urls)),
    url(r'^opsadmin/log/',include(log_url)),
    url(r'^opsadmin/test/$',testview.as_view()),

]



