from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('<int:pk>/edit/', views.student_update, name='student_update'),
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('export/csv/', views.export_students_csv, name='export_students_csv'),
    path('<int:pk>/id-card/', views.generate_id_card, name='generate_id_card'),
    path('<int:student_id>/report-card/', views.student_report_card, name='student_report_card'),
    # Bulk Operations & Promotion
    path('bulk-assign/', views.bulk_assign_classroom, name='bulk_assign_classroom'),
    path('bulk-promote/', views.bulk_promote, name='bulk_promote'),
]