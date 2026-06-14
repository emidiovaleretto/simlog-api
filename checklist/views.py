from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Aircraft, Checklist, ChecklistItem, FlightSession
from .serializers import (
    AircraftDetailSerializer,
    AircraftSerializer,
    ChecklistItemSerializer,
    ChecklistSerializer,
    FlightSessionSerializer,
)


class AircraftListCreateView(generics.ListCreateAPIView):
    serializer_class = AircraftSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Aircraft.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AircraftDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AircraftDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Aircraft.objects.filter(user=self.request.user)


class ChecklistListCreateView(generics.ListCreateAPIView):
    serializer_class = ChecklistSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Checklist.objects.filter(aircraft__user=self.request.user, aircraft_id=self.kwargs["aircraft_pk"])

    def perform_create(self, serializer):
        aircraft = Aircraft.objects.get(pk=self.kwargs["aircraft_pk"])
        if aircraft.user != self.request.user:
            raise PermissionDenied
        serializer.save(aircraft=aircraft)


class ChecklistDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChecklistSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Checklist.objects.filter(aircraft__user=self.request.user)


class ChecklistItemListCreateView(generics.ListCreateAPIView):
    serializer_class = ChecklistItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ChecklistItem.objects.filter(
            checklist__aircraft__user=self.request.user, checklist_id=self.kwargs["checklist_pk"]
        )

    def perform_create(self, serializer):
        checklist = Checklist.objects.get(pk=self.kwargs["checklist_pk"])
        if checklist.aircraft.user != self.request.user:
            raise PermissionDenied
        serializer.save(checklist=checklist)


class ChecklistItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChecklistItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ChecklistItem.objects.filter(checklist__aircraft__user=self.request.user)


class FlightSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = FlightSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return FlightSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FlightSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FlightSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return FlightSession.objects.filter(user=self.request.user)
