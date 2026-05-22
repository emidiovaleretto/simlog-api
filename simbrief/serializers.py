from rest_framework import serializers


class SimBriefFlightSerializer(serializers.Serializer):
    origin = serializers.CharField()
    destination = serializers.CharField()
    alternate = serializers.CharField()
    aircraft = serializers.CharField()
    block_fuel = serializers.FloatField()
    trip_fuel = serializers.FloatField()
    flight_level = serializers.IntegerField()
    cost_index = serializers.IntegerField()
    route = serializers.CharField()
    passengers = serializers.IntegerField()
    departure_time = serializers.CharField()
