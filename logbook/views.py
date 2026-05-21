from django.db.models import Avg

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Flight
from .serializers import FlightSerializer, FlightStatsSerializer


class FlightListCreateView(generics.ListCreateAPIView):
    serializer_class = FlightSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Flight.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FlightDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FlightSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Flight.objects.filter(user=self.request.user)


class FlightStatsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        flights = Flight.objects.filter(user=request.user)

        total_flights = flights.count()

        total_seconds = sum(
            f.duration.total_seconds()
            for f in flights
            if f.duration
        )
        total_hours = round(total_seconds / 3600, 1)

        airports = set()
        for flight in flights:
            airports.add(flight.origin)
            airports.add(flight.destination)
        airports_visited = len(airports)

        avg_score = flights.aggregate(avg=Avg("score"))["avg"]
        if avg_score:
            avg_score = round(avg_score, 1)

        stats = {
            "total_flights": total_flights,
            "total_hours": total_hours,
            "airports_visited": airports_visited,
            "avg_score": avg_score,
        }

        serializer = FlightStatsSerializer(stats)
        return Response(serializer.data)
