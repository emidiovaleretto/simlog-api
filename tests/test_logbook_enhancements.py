import pytest
from rest_framework.test import APIClient
from tests.factories import UserFactory, FlightFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.mark.django_db
class TestFlightPagination:
    def test_flight_list_is_paginated(self, authenticated_user):
        api_client, user = authenticated_user
        for _ in range(25):
            FlightFactory(user=user)
        response = api_client.get("/api/flights/")
        assert response.status_code == 200
        assert "results" in response.data
        assert "count" in response.data
        assert "next" in response.data
        assert len(response.data["results"]) == 20

    def test_flight_list_pagination_next_page(self, authenticated_user):
        api_client, user = authenticated_user
        for _ in range(25):
            FlightFactory(user=user)
        response = api_client.get("/api/flights/?page=2")
        assert response.status_code == 200
        assert "results" in response.data
        assert len(response.data["results"]) == 5


@pytest.mark.django_db
class TestFlightFiltering:
    def test_filter_flights_by_origin(self, authenticated_user):
        api_client, user = authenticated_user
        FlightFactory(user=user, origin="EIDW")
        FlightFactory(user=user, origin="EGLL")
        FlightFactory(user=user, origin="EIDW")
        response = api_client.get("/api/flights/?origin=EIDW")
        assert response.status_code == 200
        assert response.data["count"] == 2

    def test_filter_flights_by_destination(self, authenticated_user):
        api_client, user = authenticated_user
        FlightFactory(user=user, destination="EDDF")
        FlightFactory(user=user, destination="EGLL")
        response = api_client.get("/api/flights/?destination=EDDF")
        assert response.status_code == 200
        assert response.data["count"] == 1

    def test_filter_flights_by_aircraft(self, authenticated_user):
        api_client, user = authenticated_user
        FlightFactory(user=user, aircraft="A320")
        FlightFactory(user=user, aircraft="A320")
        FlightFactory(user=user, aircraft="B737")
        response = api_client.get("/api/flights/?aircraft=A320")
        assert response.status_code == 200
        assert response.data["count"] == 2


@pytest.mark.django_db
class TestFlightStatsEnhancements:
    def test_stats_returns_most_flown_aircraft(self, authenticated_user):
        api_client, user = authenticated_user
        FlightFactory(user=user, aircraft="A320")
        FlightFactory(user=user, aircraft="A320")
        FlightFactory(user=user, aircraft="B737")
        response = api_client.get("/api/flights/stats/")
        assert response.status_code == 200
        assert "most_flown_aircraft" in response.data

    def test_stats_returns_most_visited_airport(self, authenticated_user):
        api_client, user = authenticated_user
        FlightFactory(user=user, origin="EIDW", destination="EGLL")
        FlightFactory(user=user, origin="EIDW", destination="EGCC")
        FlightFactory(user=user, origin="EDDF", destination="EIDW")
        response = api_client.get("/api/flights/stats/")
        assert response.status_code == 200
        assert "most_visited_airports" in response.data
