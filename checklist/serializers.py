from rest_framework import serializers

from .models import Aircraft, Checklist, ChecklistItem, FlightSession


class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ("id", "action", "expected_value", "order", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")


class ChecklistSerializer(serializers.ModelSerializer):
    items = ChecklistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Checklist
        fields = ("id", "name", "phase", "order", "items", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")


class AircraftSerializer(serializers.ModelSerializer):
    checklists_count = serializers.SerializerMethodField()

    class Meta:
        model = Aircraft
        fields = ("id", "name", "icao_code", "checklists_count", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")

    def get_checklists_count(self, obj):
        return obj.checklists.count()


class AircraftDetailSerializer(serializers.ModelSerializer):
    checklists = ChecklistSerializer(many=True, read_only=True)

    class Meta:
        model = Aircraft
        fields = ("id", "name", "icao_code", "checklists", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")


class FlightSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightSession
        fields = ("id", "checklist", "completed_items", "started_at", "updated_at")
        read_only_fields = ("started_at", "updated_at")
