import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def jwt_token(user):
    access_token = AccessToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


@pytest.mark.django_db
def test_authenticated_user_can_access_permitted_routes(api_client, jwt_token):
    api_client.credentials(**jwt_token)
    response = api_client.get("/api/news/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthenticated_user_is_blocked(api_client):
    response = api_client.get("/api/news/")
    assert response.status_code == 401
    assert response.json()[
        "detail"] == "Authentication credentials were not provided."
