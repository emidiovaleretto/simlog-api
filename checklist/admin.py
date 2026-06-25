from django.contrib import admin
from .models import Aircraft, Checklist, \
    ChecklistItem, FlightSession

admin.site.register(Aircraft)
admin.site.register(Checklist)
admin.site.register(ChecklistItem)
admin.site.register(FlightSession)
