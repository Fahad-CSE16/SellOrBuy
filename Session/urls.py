from django.contrib import admin
from django.urls import path, include
from .views import *

# from .views import homeView, ResetPassword,ResetPasswordComplete,ResetPasswordConfirm,ResetPasswordDone

urlpatterns = [
    path('', homeView.as_view(), name='home'),
    path('signup/', handleSignup, name='signup'),
    path('activate/<uidb64>/<token>/',  activate, name='activate'),
    path('login/', handleLogin, name='login'),
    path('logout/', handleLogout, name='logout'),
    path('changepass/', changepass, name='changepass'),

    path('reset/password/', ResetPassword.as_view(), name='password_reset'),
    path('reset/password/done/', ResetPasswordDone.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirm.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', ResetPasswordComplete.as_view(),
         name='password_reset_complete'),

    path('userprofile/', userprofile, name='userprofile'),
    path('updateprofile/', updateprofile, name='updateprofile'),
    # path('otherprofile/<str:slug>/',  otherprofile, name='otherprofile'),
   

    # path('about_us/', homeView.as_view(template_name='person/about_us.html'),
    #      name='about_us'),
    # path('contact/',  contact, name='contact'),
    path('notification/',  notification, name='notification'),
    path('markasread/',  markasread, name='markasread'),
    # path('userlist/',  userlist, name='userlist'),

    # path('ajax/load-cities/',  load_cities, name='ajax_load_cities'),
]
