from rest_framework import serializers

from .models import Flight


class FlightSerializer(serializers.ModelSerializer):
    duration = serializers.DurationField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "origin",
            "destination",
            "aircraft",
            "departure_time",
            "arrival_time",
            "duration",
            "flight_level",
            "block_fuel",
            "trip_fuel",
            "efob_arrival",
            "approach_type",
            "score",
            "notes",
            "imported_from_simbrief",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("duration", "created_at", "updated_at")

    def validate_origin(self, value):
        if len(value) != 4:
            raise serializers.ValidationError("Must be a valid 4-character ICAO code.")
        return value.upper()

    def validate_destination(self, value):
        if len(value) != 4:
            raise serializers.ValidationError("Must be a valid 4-character ICAO code.")
        return value.upper()


class FlightStatsSerializer(serializers.Serializer):
    total_flights = serializers.IntegerField()
    total_hours = serializers.FloatField()
    airports_visited = serializers.IntegerField()
    avg_score = serializers.FloatField(allow_null=True)
