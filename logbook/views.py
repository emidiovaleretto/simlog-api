from django.db.models import Avg, Count

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Flight
from .serializers import FlightSerializer, FlightStatsSerializer


class FlightListCreateView(generics.ListCreateAPIView):
    serializer_class = FlightSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Flight.objects.filter(user=self.request.user)
        origin = self.request.query_params.get("origin")
        destination = self.request.query_params.get("destination")
        aircraft = self.request.query_params.get("aircraft")

        if origin:
            queryset = queryset.filter(origin__iexact=origin)
        if destination:
            queryset = queryset.filter(destination__iexact=destination)
        if aircraft:
            queryset = queryset.filter(aircraft__icontains=aircraft)

        return queryset

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

        total_seconds = sum(flight.duration.total_seconds() for flight in flights if flight.duration)
        total_hours = round(total_seconds / 3600, 1)

        airports = set()
        for flight in flights:
            airports.add(flight.origin)
            airports.add(flight.destination)
        airports_visited = len(airports)

        avg_score = flights.aggregate(avg=Avg("score"))["avg"]
        if avg_score:
            avg_score = round(avg_score, 1)

        most_flown_aircraft = flights.values("aircraft").annotate(total=Count("aircraft")).order_by("-total").first()

        most_visited_airports = sorted(
            [{"icao": icao, "count": list(airports).count(icao)} for icao in set(airports)],
            key=lambda airport: airport["count"],
            reverse=True,
        )[:5]

        stats = {
            "total_flights": total_flights,
            "total_hours": total_hours,
            "airports_visited": airports_visited,
            "avg_score": avg_score,
            "most_flown_aircraft": most_flown_aircraft,
            "most_visited_airports": most_visited_airports,
        }

        serializer = FlightStatsSerializer(stats)
        return Response(serializer.data)
