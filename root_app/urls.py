"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from . import views

app_name = "root_app"

urlpatterns = [
    path('', views.index, name='index'),
    path('letter/', views.letter, name="letter"),
    path('memo/', views.memo, name="memo"),
    path('gallery/', views.gallery, name="gallery"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    path('log/', views.log, name="log"),

    path('external_hit', views.externalHit, name="external_hit"),
    path('sitemap.xml', views.siteMap, name="sitemap"),
    path('robots.txt', views.robots, name="robots"),
    path('googleaca00d20757d854f.html', views.googleSiteVerification, name="google-site-verification"),
    path('ads.txt', views.ads, name="ads"),
]
#
