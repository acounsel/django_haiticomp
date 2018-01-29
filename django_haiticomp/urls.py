"""django_haiticomp URL Configuration

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
from django.conf.urls import url
from django.contrib import admin

from haiticomp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='input-redirect'),
    url(r'^compensation/(?P<package_id>[-\w\d]+)/(?P<language>[-\w\d]+)/$', views.view_compensation, name='package'),
    url(r'^verified/(?P<package_id>[-\w\d]+)/(?P<language>[-\w\d]+)/$', views.verify_compensation, name='verify-compensation'),
    url(r'^wrong/(?P<package_id>[-\w\d]+)/(?P<language>[-\w\d]+)/$', views.wrong_compensation, name='wrong-compensation'),
    url(r'^input/(?P<language>[-\w\d]+)/$', views.farmer_input, name='farmer-input'),
   
]
