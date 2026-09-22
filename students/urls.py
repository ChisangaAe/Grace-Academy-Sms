from django.urls import path
from . import views

urlpatterns = [
    # Dashboard / Home
    path('', views.dashboard, name='dashboard'),

    # Student Management
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('students/export/csv/', views.export_students_csv, name='export_students_csv'),
    path('students/<int:pk>/id-card/', views.generate_id_card, name='generate_id_card'),
    path('students/<int:student_id>/report-card/', views.student_report_card, name='student_report_card'),

    # Bulk Operations & Promotion
    path('students/bulk-assign/', views.bulk_assign_classroom, name='bulk_assign_classroom'),
    path('students/bulk-promote/', views.bulk_promote, name='bulk_promote'),
    path('promote/', views.promote_class, name='promote_class'),

    # Additional School Modules
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('classrooms/', views.classroom_list, name='classroom_list'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('examinations/', views.examination_list, name='examination_list'),
    path('finance/', views.finance_dashboard, name='finance_dashboard'),
    path('settings/', views.system_settings, name='system_settings'),
]