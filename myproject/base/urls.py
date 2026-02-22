from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('course_list/',course_list,name='course_list'),
    path('update/', update, name='update'),

    path('enroll_list/',enroll_list,name='enroll_list'),
    path('enroll/<int:pk>',enroll,name='enroll'),
    path('search',search,name='search'),
    path('about/',about,name='about'),
    
    
    

path('soft_delete_enroll/<int:pk>/', soft_delete_enroll, name='soft_delete_enroll'),
path('enroll_trash_list/', enroll_trash_list, name='enroll_trash_list'),
path('permanent_delete_enroll/<int:pk>/', permanent_delete_enroll, name='permanent_delete_enroll'),
path('restore/<int:pk>/',restore,name='restore')

]