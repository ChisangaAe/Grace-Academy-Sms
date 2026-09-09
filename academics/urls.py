from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.classroom_list, name='academics_home'),
    path('classrooms/', views.classroom_list, name='classroom_list'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('marks/enter/', views.enter_marks, name='enter_marks'),
    path('enter-marks/', views.enter_marks, name='enter_marks'),
    path('enter-behavior/', views.enter_behavior, name='enter_behavior'),
    path('my-timetable/', views.my_timetable, name='my_timetable'),
    path('classrooms/<int:classroom_id>/timetable/', views.classroom_timetable, name='classroom_timetable'),
    path('timetable/delete/<int:slot_id>/', views.delete_timetable_slot, name='delete_timetable_slot'),
]