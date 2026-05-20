from django.db import models
from django.contrib.auth.models import User


class Aircraft(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="aircraft")
    name = models.CharField(max_length=50)
    icao_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.icao_code})"


class Checklist(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name="checklists")
    name = models.CharField(max_length=50)
    phase = models.CharField(max_length=30)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.aircraft.name} — {self.name}"


class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name="items")
    action = models.CharField(max_length=100)
    expected_value = models.CharField(max_length=50, blank=True, default="")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.action} — {self.expected_value}"


class FlightSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name="sessions")
    completed_items = models.JSONField(default=list)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} — {self.checklist.name} ({self.started_at.date()})"
