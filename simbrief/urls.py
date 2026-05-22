from django.urls import path

from .views import SimBriefImportView, SimBriefLatestView

urlpatterns = [
    path("latest/", SimBriefLatestView.as_view(), name="simbrief-latest"),
    path("import/", SimBriefImportView.as_view(), name="simbrief-import"),
]
