# config/urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Changed 'admin.site.py_admin' to 'admin.site.urls'
    path('admin/', admin.site.urls),
]

# This allows the browser to show the medical files you upload
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)