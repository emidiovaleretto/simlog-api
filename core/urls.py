from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from django.conf.urls.static import static
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/flights/", include("logbook.urls")),
    path("api/simbrief/", include("simbrief.urls")),
    path("api/", include("checklist.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(
        url_name="schema",
        ),
        name="swagger-ui"),
    path("", RedirectView.as_view(pattern_name="swagger-ui")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
