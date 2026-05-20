from django.urls import path

from .views import FlightDetailView, FlightListCreateView, FlightStatsView

urlpatterns = [
    path("", FlightListCreateView.as_view(), name="flight-list-create"),
    path("<int:pk>/", FlightDetailView.as_view(), name="flight-detail"),
    path("stats/", FlightStatsView.as_view(), name="flight-stats"),
]
