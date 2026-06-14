from django.utils import timezone

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from logbook.models import Flight
from .serializers import SimBriefFlightSerializer
from .services import SimBriefService


class SimBriefLatestView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        pilot_id = request.user.profile.simbrief_pilot_id

        if not pilot_id:
            return Response(
                {"detail": "SimBrief pilot ID not configured. Update your profile first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            flight_data = SimBriefService.fetch_latest_flight(pilot_id)
        except Exception:
            return Response(
                {"detail": "SimBrief API is unreachable. Please try again later."}, status=status.HTTP_502_BAD_GATEWAY
            )

        serializer = SimBriefFlightSerializer(flight_data)
        return Response(serializer.data)


class SimBriefImportView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        pilot_id = request.user.profile.simbrief_pilot_id

        if not pilot_id:
            return Response(
                {"detail": "SimBrief pilot ID not configured. Update your profile first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            flight_data = SimBriefService.fetch_latest_flight(pilot_id)
        except Exception:
            return Response(
                {"detail": "SimBrief API is unreachable. Please try again later."}, status=status.HTTP_502_BAD_GATEWAY
            )

        flight, created = Flight.objects.get_or_create(
            user=request.user,
            origin=flight_data["origin"],
            destination=flight_data["destination"],
            flight_level=flight_data["flight_level"],
            defaults={
                "aircraft": flight_data["aircraft"],
                "block_fuel": flight_data["block_fuel"],
                "trip_fuel": flight_data["trip_fuel"],
                "departure_time": timezone.now(),
                "imported_from_simbrief": True,
            },
        )

        from logbook.serializers import FlightSerializer

        serializer = FlightSerializer(flight)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)
