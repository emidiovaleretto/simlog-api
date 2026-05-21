import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from tests.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.mark.django_db
class TestRegisterEndpoint:
    def test_register_with_valid_data_returns_201(self, api_client):
        payload = {
            "username": "emidio",
            "email": "emidio@test.com",
            "password": "test1234"
        }
        response = api_client.post("/api/auth/register/", payload, format="json")
        assert response.status_code == 201

    def test_register_creates_user_in_database(self, api_client):
        payload = {
            "username": "emidio",
            "email": "emidio@test.com",
            "password": "test1234"
        }
        api_client.post("/api/auth/register/", payload, format="json")
        assert User.objects.filter(username="emidio").exists()

    def test_register_creates_user_profile_automatically(self, api_client):
        payload = {
            "username": "emidio",
            "email": "emidio@test.com",
            "password": "test1234"
        }
        api_client.post("/api/auth/register/", payload, format="json")
        user = User.objects.get(username="emidio")
        assert hasattr(user, "profile")

    def test_register_with_duplicate_username_returns_400(self, api_client):
        UserFactory(username="emidio")
        payload = {
            "username": "emidio",
            "email": "outro@test.com",
            "password": "test1234"
        }
        response = api_client.post("/api/auth/register/", payload, format="json")
        assert response.status_code == 400

    def test_register_with_short_password_returns_400(self, api_client):
        payload = {
            "username": "emidio",
            "email": "emidio@test.com",
            "password": "123"
        }
        response = api_client.post("/api/auth/register/", payload, format="json")
        assert response.status_code == 400

    def test_register_without_username_returns_400(self, api_client):
        payload = {
            "email": "emidio@test.com",
            "password": "test1234"
        }
        response = api_client.post("/api/auth/register/", payload, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestLoginEndpoint:
    def test_login_with_valid_credentials_returns_200(self, api_client):
        UserFactory(username="emidio")
        payload = {"username": "emidio", "password": "test1234"}
        response = api_client.post("/api/auth/login/", payload, format="json")
        assert response.status_code == 200

    def test_login_returns_access_and_refresh_tokens(self, api_client):
        UserFactory(username="emidio")
        payload = {"username": "emidio", "password": "test1234"}
        response = api_client.post("/api/auth/login/", payload, format="json")
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_with_wrong_password_returns_401(self, api_client):
        UserFactory(username="emidio")
        payload = {"username": "emidio", "password": "wrongpassword"}
        response = api_client.post("/api/auth/login/", payload, format="json")
        assert response.status_code == 401

    def test_login_with_nonexistent_user_returns_401(self, api_client):
        payload = {"username": "ghost", "password": "test1234"}
        response = api_client.post("/api/auth/login/", payload, format="json")
        assert response.status_code == 401


@pytest.mark.django_db
class TestMeEndpoint:
    def test_me_returns_200_for_authenticated_user(self, authenticated_client):
        client, user = authenticated_client
        response = client.get("/api/auth/me/")
        assert response.status_code == 200

    def test_me_returns_correct_user_data(self, authenticated_client):
        client, user = authenticated_client
        response = client.get("/api/auth/me/")
        assert response.data["username"] == user.username
        assert response.data["email"] == user.email

    def test_me_returns_401_for_unauthenticated_user(self, api_client):
        response = api_client.get("/api/auth/me/")
        assert response.status_code == 401

    def test_me_update_simbrief_pilot_id_returns_200(self, authenticated_client):
        client, user = authenticated_client
        payload = {"profile": {"simbrief_pilot_id": "216664"}}
        response = client.put("/api/auth/me/", payload, format="json")
        assert response.status_code == 200

    def test_me_update_saves_simbrief_pilot_id(self, authenticated_client):
        client, user = authenticated_client
        payload = {"profile": {"simbrief_pilot_id": "216664"}}
        client.put("/api/auth/me/", payload, format="json")
        user.profile.refresh_from_db()
        assert user.profile.simbrief_pilot_id == "216664"
