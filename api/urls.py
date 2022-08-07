from django.urls import path
from . import views

urlpatterns = [
    path('',views.getRoutes,name='routes'), #shows routes
    path('users/',views.getUsers,name='users'), #shows users
    path('codes/',views.getPythonCode,name='codes'),    #shows python codes
]