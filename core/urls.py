from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/flights/", include("logbook.urls")),
    path("api/simbrief/", include("simbrief.urls")),
    path("api/", include("checklist.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
