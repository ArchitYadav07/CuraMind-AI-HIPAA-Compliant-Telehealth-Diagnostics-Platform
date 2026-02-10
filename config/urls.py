from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # This connects your diagnostics app to the project
    path('diagnostics/', include('apps.diagnostics.urls')),

    path('accounts/', include('django.contrib.auth.urls')),
]

# This allows the browser to actually 'see' the uploaded X-rays
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)