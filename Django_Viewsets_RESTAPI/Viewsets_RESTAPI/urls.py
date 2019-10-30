"""Viewsets_RESTAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
# from musics import views  # If import mutiple models at the same time, can't write this way.
from musics.views import MusicViewSet
from shares.views import ShareViewSet

router = DefaultRouter()
router.register(r'music', MusicViewSet, base_name='music')
router.register(r'shares', ShareViewSet, base_name='share')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls), name="api"),
    # path("api/", include("languages.urls")),
    path("", include("languages.urls")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))      # Adding this line will make the login button show up
]
