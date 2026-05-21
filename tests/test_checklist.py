import pytest
from rest_framework.test import APIClient

from tests.factories import (
    AircraftFactory,
    ChecklistFactory,
    ChecklistItemFactory,
    FlightSessionFactory,
    UserFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.mark.django_db
class TestAircraftEndpoint:
    def test_create_aircraft_returns_201(self, authenticated_client):
        client, user = authenticated_client
        payload = {"name": "Fenix A320", "icao_code": "A320"}
        response = client.post("/api/aircraft/", payload, format="json")
        assert response.status_code == 201

    def test_create_aircraft_saves_correct_user(self, authenticated_client):
        client, user = authenticated_client
        payload = {"name": "Fenix A320", "icao_code": "A320"}
        client.post("/api/aircraft/", payload, format="json")
        assert user.aircraft.filter(name="Fenix A320").exists()

    def test_list_aircraft_returns_only_authenticated_user_aircraft(self, api_client):
        user_one = UserFactory()
        user_two = UserFactory()
        AircraftFactory(user=user_one)
        AircraftFactory(user=user_one)
        AircraftFactory(user=user_two)
        api_client.force_authenticate(user=user_one)
        response = api_client.get("/api/aircraft/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_retrieve_aircraft_with_checklists_returns_200(self, authenticated_client):
        client, user = authenticated_client
        aircraft = AircraftFactory(user=user)
        ChecklistFactory(aircraft=aircraft)
        response = client.get(f"/api/aircraft/{aircraft.id}/")
        assert response.status_code == 200
        assert len(response.data["checklists"]) == 1

    def test_retrieve_another_user_aircraft_returns_404(self, authenticated_client):
        client, user = authenticated_client
        another_user = UserFactory()
        aircraft = AircraftFactory(user=another_user)
        response = client.get(f"/api/aircraft/{aircraft.id}/")
        assert response.status_code == 404

    def test_delete_aircraft_returns_204(self, authenticated_client):
        client, user = authenticated_client
        aircraft = AircraftFactory(user=user)
        response = client.delete(f"/api/aircraft/{aircraft.id}/")
        assert response.status_code == 204

    def test_create_aircraft_returns_401_for_unauthenticated_user(self, api_client):
        payload = {"name": "Fenix A320", "icao_code": "A320"}
        response = api_client.post("/api/aircraft/", payload, format="json")
        assert response.status_code == 401


@pytest.mark.django_db
class TestChecklistEndpoint:
    def test_create_checklist_returns_201(self, authenticated_client):
        client, user = authenticated_client
        aircraft = AircraftFactory(user=user)
        payload = {"name": "Before Start", "phase": "pre-departure", "order": 1}
        response = client.post(f"/api/aircraft/{aircraft.id}/checklists/", payload, format="json")
        assert response.status_code == 201

    def test_create_checklist_for_another_user_aircraft_returns_403(self, authenticated_client):
        client, user = authenticated_client
        another_user = UserFactory()
        aircraft = AircraftFactory(user=another_user)
        payload = {"name": "Before Start", "phase": "pre-departure", "order": 1}
        response = client.post(f"/api/aircraft/{aircraft.id}/checklists/", payload, format="json")
        assert response.status_code == 403

    def test_list_checklists_returns_only_aircraft_checklists(self, authenticated_client):
        client, user = authenticated_client
        aircraft = AircraftFactory(user=user)
        ChecklistFactory(aircraft=aircraft)
        ChecklistFactory(aircraft=aircraft)
        response = client.get(f"/api/aircraft/{aircraft.id}/checklists/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_retrieve_checklist_with_items_returns_200(self, authenticated_client):
        client, user = authenticated_client
        aircraft = AircraftFactory(user=user)
        checklist = ChecklistFactory(aircraft=aircraft)
        ChecklistItemFactory(checklist=checklist)
        ChecklistItemFactory(checklist=checklist)
        response = client.get(f"/api/checklists/{checklist.id}/")
        assert response.status_code == 200
        assert len(response.data["items"]) == 2

    def test_delete_checklist_returns_204(self, authenticated_client):
        client, user = authenticated_client
        aircraft = AircraftFactory(user=user)
        checklist = ChecklistFactory(aircraft=aircraft)
        response = client.delete(f"/api/checklists/{checklist.id}/")
        assert response.status_code == 204


@pytest.mark.django_db
class TestChecklistItemEndpoint:
    def test_create_item_returns_201(self, authenticated_client):
        client, user = authenticated_client
        aircraft = AircraftFactory(user=user)
        checklist = ChecklistFactory(aircraft=aircraft)
        payload = {"action": "Parking brake", "expected_value": "SET", "order": 1}
        response = client.post(f"/api/checklists/{checklist.id}/items/", payload, format="json")
        assert response.status_code == 201

    def test_create_item_for_another_user_checklist_returns_403(self, authenticated_client):
        client, user = authenticated_client
        another_user = UserFactory()
        aircraft = AircraftFactory(user=another_user)
        checklist = ChecklistFactory(aircraft=aircraft)
        payload = {"action": "Parking brake", "expected_value": "SET", "order": 1}
        response = client.post(f"/api/checklists/{checklist.id}/items/", payload, format="json")
        assert response.status_code == 403

    def test_list_items_returns_only_checklist_items(self, authenticated_client):
        client, user = authenticated_client
        aircraft = AircraftFactory(user=user)
        checklist = ChecklistFactory(aircraft=aircraft)
        ChecklistItemFactory(checklist=checklist)
        ChecklistItemFactory(checklist=checklist)
        response = client.get(f"/api/checklists/{checklist.id}/items/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_delete_item_returns_204(self, authenticated_client):
        client, user = authenticated_client
        aircraft = AircraftFactory(user=user)
        checklist = ChecklistFactory(aircraft=aircraft)
        item = ChecklistItemFactory(checklist=checklist)
        response = client.delete(f"/api/items/{item.id}/")
        assert response.status_code == 204


@pytest.mark.django_db
class TestFlightSessionEndpoint:
    def test_create_session_returns_201(self, authenticated_client):
        client, user = authenticated_client
        aircraft = AircraftFactory(user=user)
        checklist = ChecklistFactory(aircraft=aircraft)
        payload = {"checklist": checklist.id, "completed_items": []}
        response = client.post("/api/sessions/", payload, format="json")
        assert response.status_code == 201

    def test_update_session_completed_items_returns_200(self, authenticated_client):
        client, user = authenticated_client
        aircraft = AircraftFactory(user=user)
        checklist = ChecklistFactory(aircraft=aircraft)
        item = ChecklistItemFactory(checklist=checklist)
        session = FlightSessionFactory(user=user, checklist=checklist)
        payload = {"completed_items": [item.id]}
        response = client.patch(f"/api/sessions/{session.id}/", payload, format="json")
        assert response.status_code == 200
        assert item.id in response.data["completed_items"]

    def test_retrieve_session_returns_200(self, authenticated_client):
        client, user = authenticated_client
        aircraft = AircraftFactory(user=user)
        checklist = ChecklistFactory(aircraft=aircraft)
        session = FlightSessionFactory(user=user, checklist=checklist)
        response = client.get(f"/api/sessions/{session.id}/")
        assert response.status_code == 200

    def test_retrieve_another_user_session_returns_404(self, authenticated_client):
        client, user = authenticated_client
        another_user = UserFactory()
        aircraft = AircraftFactory(user=another_user)
        checklist = ChecklistFactory(aircraft=aircraft)
        session = FlightSessionFactory(user=another_user, checklist=checklist)
        response = client.get(f"/api/sessions/{session.id}/")
        assert response.status_code == 404
