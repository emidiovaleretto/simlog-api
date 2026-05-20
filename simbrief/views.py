from django.shortcuts import render
from django.http import JsonResponse
from .services import SimBriefService

def index(request):
    response = SimBriefService.fetch_latest_flight(216664)
    return JsonResponse(response)
