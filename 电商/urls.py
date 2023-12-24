"""
URL configuration for 电商 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('register/', views.register),
    path('buymainpage/',views.buymainpage),
    path('logout/',views.logout),
    path('search/',views.search),
    path('image/',views.image),
    path('put/',views.put),
    path('<int:nid>/detailshow/',views.detailshow),
    path('suiji/',views.suiji),
    path('<int:nid>/next/',views.next),
    path('<int:nid>/last/',views.last),
    path('<int:nid>/comment/',views.comment),
    path('<int:nid>/recomment/',views.recomment),
    path('<int:nid>/delete/',views.delete),
    path('history/', views.history),
    path('myinformation/', views.myinformation),
    path('houtai/', views.houtai),
    path('<int:nid>/guandelete/',views.guandelete),
    path('',views.welcome),

]
