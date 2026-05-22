import pytest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient

from tests.factories import UserFactory


SIMBRIEF_MOCK_RESPONSE = {
    "origin": {"icao_code": "EIDW"},
    "destination": {"icao_code": "KJFK"},
    "alternate": {"icao_code": "KBOS"},
    "aircraft": {"icaocode": "A320"},
    "fuel": {
        "plan_ramp": "18970",
        "enroute_burn": "17284",
    },
    "general": {
        "initial_altitude": "34000",
        "costindex": "12",
        "route": "EIDW DCT KJFK",
    },
    "weights": {
        "pax_count": "180",
        "payload": "19982",
    },
    "times": {
        "sched_out": "1716300000",
    },
}


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = UserFactory()
    user.profile.simbrief_pilot_id = "216664"
    user.profile.save()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def authenticated_client_without_pilot_id(api_client):
    user = UserFactory()
    user.profile.simbrief_pilot_id = ""
    user.profile.save()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.mark.django_db
class TestSimBriefLatestEndpoint:
    @patch("simbrief.services.requests.get")
    def test_fetch_latest_flight_returns_200(self, mock_get, authenticated_client):
        mock_response = MagicMock()
        mock_response.json.return_value = SIMBRIEF_MOCK_RESPONSE
        mock_get.return_value = mock_response

        client, user = authenticated_client
        response = client.get("/api/simbrief/latest/")
        assert response.status_code == 200

    @patch("simbrief.services.requests.get")
    def test_fetch_latest_flight_returns_correct_data(self, mock_get, authenticated_client):
        mock_response = MagicMock()
        mock_response.json.return_value = SIMBRIEF_MOCK_RESPONSE
        mock_get.return_value = mock_response

        client, user = authenticated_client
        response = client.get("/api/simbrief/latest/")
        assert response.data["origin"] == "EIDW"
        assert response.data["destination"] == "KJFK"
        assert response.data["aircraft"] == "A320"
        assert response.data["block_fuel"] == 18970.0
        assert response.data["trip_fuel"] == 17284.0

    def test_fetch_latest_flight_returns_400_without_pilot_id(
        self, authenticated_client_without_pilot_id
    ):
        client, user = authenticated_client_without_pilot_id
        response = client.get("/api/simbrief/latest/")
        assert response.status_code == 400

    def test_fetch_latest_flight_returns_401_for_unauthenticated_user(self, api_client):
        response = api_client.get("/api/simbrief/latest/")
        assert response.status_code == 401

    @patch("simbrief.services.requests.get")
    def test_fetch_latest_flight_returns_502_when_simbrief_is_unreachable(
        self, mock_get, authenticated_client
    ):
        mock_get.side_effect = Exception("Connection error")
        client, user = authenticated_client
        response = client.get("/api/simbrief/latest/")
        assert response.status_code == 502


@pytest.mark.django_db
class TestSimBriefImportEndpoint:
    @patch("simbrief.services.requests.get")
    def test_import_flight_returns_201(self, mock_get, authenticated_client):
        mock_response = MagicMock()
        mock_response.json.return_value = SIMBRIEF_MOCK_RESPONSE
        mock_get.return_value = mock_response

        client, user = authenticated_client
        response = client.post("/api/simbrief/import/")
        assert response.status_code == 201

    @patch("simbrief.services.requests.get")
    def test_import_flight_creates_flight_in_database(self, mock_get, authenticated_client):
        mock_response = MagicMock()
        mock_response.json.return_value = SIMBRIEF_MOCK_RESPONSE
        mock_get.return_value = mock_response

        client, user = authenticated_client
        client.post("/api/simbrief/import/")

        from logbook.models import Flight
        assert Flight.objects.filter(user=user, origin="EIDW", destination="KJFK").exists()

    @patch("simbrief.services.requests.get")
    def test_import_flight_sets_imported_from_simbrief_true(self, mock_get, authenticated_client):
        mock_response = MagicMock()
        mock_response.json.return_value = SIMBRIEF_MOCK_RESPONSE
        mock_get.return_value = mock_response

        client, user = authenticated_client
        client.post("/api/simbrief/import/")

        from logbook.models import Flight
        flight = Flight.objects.get(user=user, origin="EIDW")
        assert flight.imported_from_simbrief is True

    @patch("simbrief.services.requests.get")
    def test_import_flight_twice_returns_existing_flight(self, mock_get, authenticated_client):
        mock_response = MagicMock()
        mock_response.json.return_value = SIMBRIEF_MOCK_RESPONSE
        mock_get.return_value = mock_response

        client, user = authenticated_client
        client.post("/api/simbrief/import/")
        response = client.post("/api/simbrief/import/")

        from logbook.models import Flight
        assert Flight.objects.filter(user=user).count() == 1
        assert response.status_code == 200

    def test_import_flight_returns_400_without_pilot_id(
        self, authenticated_client_without_pilot_id
    ):
        client, user = authenticated_client_without_pilot_id
        response = client.post("/api/simbrief/import/")
        assert response.status_code == 400
