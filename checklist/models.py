from django.db import models
from django.contrib.auth.models import User


class Aircraft(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    icao_code = models.CharField(max_length=6)


class Checklist(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phase = models.CharField(max_length=30)
    order = models.IntegerField()


class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    expected_value = models.CharField(max_length=50)
    order = models.IntegerField()
