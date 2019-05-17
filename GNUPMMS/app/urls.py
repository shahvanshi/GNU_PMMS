"""GNUPMMS URL Configuration

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
from django.urls import path, include
from django.views.generic.base import TemplateView # new
from django.conf.urls import url
from app import views
#from django.contrib.auth.views import login,logout

urlpatterns = [

    path('',views.login),
    path('app/',views.login), # new
    path('app/externalRegistration',views.externalRegistration),
    path('app/viewExternalUser',views.viewExternalUser),
    path('app/studentDashboard',views.studentDashboard),
    path('app/stageDetails/<id>',views.stageDetails),
    path('app/facultyDashboard',views.facultyDashboard),
    path('app/stageApproval/<id>',views.facultyApproval),
    path('app/login/',views.login),
    path('app/logout/',views.logout),
    path('app/studentRegistration/',views.studentRegistration),
    path('app/loginRegistration/',views.loginRegistration),
    path('app/registerProject/',views.registerProject),


    #url(r'^login/$', auth_views.login, name='login'),

    #url(r'^logout/$', auth_views.logout, name='logout'),

]
