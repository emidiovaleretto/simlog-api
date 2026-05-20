from django.urls import path

from .views import (
    AircraftDetailView,
    AircraftListCreateView,
    ChecklistDetailView,
    ChecklistItemDetailView,
    ChecklistItemListCreateView,
    ChecklistListCreateView,
    FlightSessionDetailView,
    FlightSessionListCreateView,
)

urlpatterns = [
    path("aircraft/", AircraftListCreateView.as_view(), name="aircraft-list-create"),
    path("aircraft/<int:pk>/", AircraftDetailView.as_view(), name="aircraft-detail"),
    path("aircraft/<int:aircraft_pk>/checklists/", ChecklistListCreateView.as_view(), name="checklist-list-create"),
    path("checklists/<int:pk>/", ChecklistDetailView.as_view(), name="checklist-detail"),
    path("checklists/<int:checklist_pk>/items/", ChecklistItemListCreateView.as_view(), name="item-list-create"),
    path("items/<int:pk>/", ChecklistItemDetailView.as_view(), name="item-detail"),
    path("sessions/", FlightSessionListCreateView.as_view(), name="session-list-create"),
    path("sessions/<int:pk>/", FlightSessionDetailView.as_view(), name="session-detail"),
]
