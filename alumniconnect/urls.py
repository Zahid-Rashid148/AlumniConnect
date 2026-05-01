from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin Customization
admin.site.site_header = "AlumniConnect® Control Center"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "System Management"
