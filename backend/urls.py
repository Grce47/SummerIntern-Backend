from django.contrib import admin
from django.urls import path,include
import myUser.views as User_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('signup/',User_views.signup,name='myUser-signup'),   
    path('login/',User_views.MyLoginView.as_view(),name='myUser-login'),   
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='myUser-logout'), 
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'), 
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'), 
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'), 
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'), 
    path('api/',include('api.urls')),
    path('list_codes/',User_views.listcodes,name='myUser-listcodes'),
    path('download/',User_views.download_data,name='myUser-download'),
    path('detail_code/',User_views.detailcodes,name='myUser-detailcode'),
    path('detail_code/<int:index>',User_views.detailcodes,name='User-detailcode'),
    path('',User_views.course,name='Course-home'),
    path('<int:index>',User_views.course,name='Course-home'),
]
