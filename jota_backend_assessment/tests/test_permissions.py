import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username="admin", password="adminpass")


@pytest.fixture
def reader_user(db):
    return User.objects.create_user(username="reader", password="readerpass")


@pytest.fixture
def admin_token(admin_user):
    access_token = AccessToken.for_user(admin_user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


@pytest.fixture
def reader_token(reader_user):
    access_token = AccessToken.for_user(reader_user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


@pytest.mark.django_db
def test_admin_has_full_access(api_client, admin_token):
    response = api_client.get("/api/news/", **admin_token)
    assert response.status_code == 200
