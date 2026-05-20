from django.db import models
from django.contrib.auth.models import User


class Flight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=4)
    destination = models.CharField(max_length=4)
    aircraft = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    duration = models.DurationField()
    flight_level = models.IntegerField()
    block_fuel = models.FloatField()
    efob_arrival = models.FloatField()
    approach_type = models.CharField(max_length=20)
    score = models.FloatField(null=True)
    status = models.CharField(max_length=10)
    notes = models.TextField(blank=True)
    is_imported_from_simbrief = models.BooleanField(default=False)
