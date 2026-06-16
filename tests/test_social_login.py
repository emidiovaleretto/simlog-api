import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient


@pytest.mark.django_db
class TestSocialLoginEndpoint:
    def test_endpoint_without_token_returns_status_code_400(self):
        client = APIClient()
        response = client.post("/api/auth/google/", format="json")
        assert response.status_code == 400
