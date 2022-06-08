"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
import myUser.views as User_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('signup/',User_views.signup,name='myUser-signup'),   
    path('login/',User_views.MyLoginView.as_view(),name='myUser-login'),   
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='myUser-logout'), 
    path('api/',include('api.urls')),
    path('list_codes/',User_views.listcodes,name='myUser-listcodes'),
    path('download/',User_views.download_data,name='myUser-download'),
    path('detail_code/',User_views.detailcodes,name='myUser-detailcode'),
    path('detail_code/<int:index>',User_views.detailcodes,name='User-detailcode'),

    path('',User_views.course,name='Course-home'),
    path('<int:index>',User_views.course,name='Course-home'),
]
