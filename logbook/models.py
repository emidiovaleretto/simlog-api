from django.db import models
from django.contrib.auth.models import User


class Flight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="flights")
    origin = models.CharField(max_length=4)
    destination = models.CharField(max_length=4)
    aircraft = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    flight_level = models.IntegerField(null=True, blank=True)
    block_fuel = models.FloatField(null=True, blank=True)
    trip_fuel = models.FloatField(null=True, blank=True)
    efob_arrival = models.FloatField(null=True, blank=True)
    approach_type = models.CharField(max_length=20, blank=True, default="")
    score = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    imported_from_simbrief = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-departure_time"]

    def __str__(self):
        return f"{self.origin} -> {self.destination} ({self.departure_time.date()})"

    def save(self, *args, **kwargs):
        if self.departure_time and self.arrival_time:
            self.duration = self.arrival_time - self.departure_time
        super().save(*args, **kwargs)
