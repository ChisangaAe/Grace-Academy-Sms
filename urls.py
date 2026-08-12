from django.contrib import admin
from django.urls import path, include
from accounts.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('students/', include('students.urls')),
    path('academics/', include('academics.urls')),
    path('attendance/', include('attendance.urls')),
    path('grades/', include('grades.urls')),
    path('accounts/', include('accounts.urls')),
]