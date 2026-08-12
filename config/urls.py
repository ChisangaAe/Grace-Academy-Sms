from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import dashboard

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Main Dashboard
    path('', dashboard, name='dashboard'),

    # Application URLs (Delegated to each app's urls.py)
    path('students/', include('students.urls')),
    path('academics/', include('academics.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)