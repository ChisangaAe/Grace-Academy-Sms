from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.classroom_list, name='academics_home'),
    path('classrooms/', views.classroom_list, name='classroom_list'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('marks/enter/', views.enter_marks, name='enter_marks'),
]