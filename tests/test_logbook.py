import pytest
from rest_framework.test import APIClient

from tests.factories import FlightFactory, UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.mark.django_db
class TestFlightListCreateEndpoint:
    def test_create_flight_with_valid_data_returns_201(self, authenticated_client):
        client, user = authenticated_client
        payload = {
            "origin": "EIDW",
            "destination": "LEIB",
            "aircraft": "Fenix A320",
            "departure_time": "2026-05-20T10:00:00Z",
            "arrival_time": "2026-05-20T12:30:00Z",
            "flight_level": 280,
            "score": 99.0,
            "notes": "Great flight!",
        }
        response = client.post("/api/flights/", payload, format="json")
        assert response.status_code == 201

    def test_create_flight_saves_correct_user(self, authenticated_client):
        client, user = authenticated_client
        payload = {
            "origin": "EIDW",
            "destination": "LEIB",
            "aircraft": "Fenix A320",
            "departure_time": "2026-05-20T10:00:00Z",
            "arrival_time": "2026-05-20T12:30:00Z",
            "flight_level": 280,
        }
        response = client.post("/api/flights/", payload, format="json")
        assert response.data["origin"] == "EIDW"

    def test_create_flight_calculates_duration_automatically(self, authenticated_client):
        client, user = authenticated_client
        payload = {
            "origin": "EIDW",
            "destination": "LEIB",
            "aircraft": "Fenix A320",
            "departure_time": "2026-05-20T10:00:00Z",
            "arrival_time": "2026-05-20T12:30:00Z",
            "flight_level": 280,
        }
        response = client.post("/api/flights/", payload, format="json")
        assert response.data["duration"] == "02:30:00"

    def test_create_flight_uppercases_icao_codes(self, authenticated_client):
        client, user = authenticated_client
        payload = {
            "origin": "eidw",
            "destination": "leib",
            "aircraft": "Fenix A320",
            "departure_time": "2026-05-20T10:00:00Z",
            "flight_level": 280,
        }
        response = client.post("/api/flights/", payload, format="json")
        assert response.data["origin"] == "EIDW"
        assert response.data["destination"] == "LEIB"

    def test_create_flight_with_invalid_icao_returns_400(self, authenticated_client):
        client, user = authenticated_client
        payload = {
            "origin": "INVALID",
            "destination": "LEIB",
            "aircraft": "Fenix A320",
            "departure_time": "2026-05-20T10:00:00Z",
            "flight_level": 280,
        }
        response = client.post("/api/flights/", payload, format="json")
        assert response.status_code == 400

    def test_create_flight_returns_401_for_unauthenticated_user(self, api_client):
        payload = {
            "origin": "EIDW",
            "destination": "LEIB",
            "aircraft": "Fenix A320",
            "departure_time": "2026-05-20T10:00:00Z",
            "flight_level": 280,
        }
        response = api_client.post("/api/flights/", payload, format="json")
        assert response.status_code == 401

    def test_list_flights_returns_only_authenticated_user_flights(self, api_client):
        user_one = UserFactory()
        user_two = UserFactory()
        FlightFactory(user=user_one)
        FlightFactory(user=user_one)
        FlightFactory(user=user_two)
        api_client.force_authenticate(user=user_one)
        response = api_client.get("/api/flights/")
        assert response.status_code == 200
        assert response.data["count"] == 2

    def test_list_flights_returns_empty_list_when_no_flights(self, authenticated_client):
        client, user = authenticated_client
        response = client.get("/api/flights/")
        assert response.status_code == 200
        assert response.data["count"] == 0


@pytest.mark.django_db
class TestFlightDetailEndpoint:
    def test_retrieve_flight_returns_200(self, authenticated_client):
        client, user = authenticated_client
        flight = FlightFactory(user=user)
        response = client.get(f"/api/flights/{flight.id}/")
        assert response.status_code == 200

    def test_retrieve_flight_returns_correct_data(self, authenticated_client):
        client, user = authenticated_client
        flight = FlightFactory(user=user, origin="EIDW", destination="KJFK")
        response = client.get(f"/api/flights/{flight.id}/")
        assert response.data["origin"] == "EIDW"
        assert response.data["destination"] == "KJFK"

    def test_retrieve_another_user_flight_returns_404(self, authenticated_client):
        client, user = authenticated_client
        another_user = UserFactory()
        flight = FlightFactory(user=another_user)
        response = client.get(f"/api/flights/{flight.id}/")
        assert response.status_code == 404

    def test_update_flight_notes_returns_200(self, authenticated_client):
        client, user = authenticated_client
        flight = FlightFactory(user=user)
        payload = {"notes": "Updated notes"}
        response = client.patch(f"/api/flights/{flight.id}/", payload, format="json")
        assert response.status_code == 200

    def test_delete_flight_returns_204(self, authenticated_client):
        client, user = authenticated_client
        flight = FlightFactory(user=user)
        response = client.delete(f"/api/flights/{flight.id}/")
        assert response.status_code == 204


@pytest.mark.django_db
class TestFlightStatsEndpoint:
    def test_stats_returns_200(self, authenticated_client):
        client, user = authenticated_client
        response = client.get("/api/flights/stats/")
        assert response.status_code == 200

    def test_stats_returns_correct_total_flights(self, authenticated_client):
        client, user = authenticated_client
        FlightFactory(user=user)
        FlightFactory(user=user)
        FlightFactory(user=user)
        response = client.get("/api/flights/stats/")
        assert response.data["total_flights"] == 3

    def test_stats_returns_zero_when_no_flights(self, authenticated_client):
        client, user = authenticated_client
        response = client.get("/api/flights/stats/")
        assert response.data["total_flights"] == 0
        assert response.data["total_hours"] == 0
        assert response.data["airports_visited"] == 0
        assert response.data["avg_score"] is None

    def test_stats_counts_unique_airports(self, authenticated_client):
        client, user = authenticated_client
        FlightFactory(user=user, origin="EIDW", destination="LEIB")
        FlightFactory(user=user, origin="LEIB", destination="LEBB")
        response = client.get("/api/flights/stats/")
        assert response.data["airports_visited"] == 3
