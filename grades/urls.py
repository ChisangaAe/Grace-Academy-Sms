from django.urls import path
from . import views

urlpatterns = [
    path('', views.grade_list, name='grade_list'),
    path('add/', views.add_grade, name='add_grade'),
]