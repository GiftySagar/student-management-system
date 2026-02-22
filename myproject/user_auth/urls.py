from django.urls import path

from .views import *

urlpatterns = [
    path('',login_,name='login_'),
    path('register/',register,name='register'),
    path('logout_/',logout_,name='logout_'),
    path('profile/',profile,name='profile'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('reset/',reset,name='reset'),
    path('new_password',new_password,name='new_password')
]