import pytest
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from news_api.models import News
from django.utils import timezone


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(username="regular_user", password="password123")


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username="admin", password="admin123")


@pytest.fixture
def editor_user(db):
    user = User.objects.create_user(username="editor", password="password123")
    editor_group, _ = Group.objects.get_or_create(name="Editor")
    user.groups.add(editor_group)
    return user


@pytest.fixture
def regular_token(regular_user):
    access_token = AccessToken.for_user(regular_user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


@pytest.fixture
def admin_token(admin_user):
    access_token = AccessToken.for_user(admin_user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


@pytest.fixture
def editor_token(editor_user):
    access_token = AccessToken.for_user(editor_user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_protected_routes(api_client):
    response = api_client.get("/api/news/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_regular_user_cannot_create_news(api_client, regular_token):
    api_client.credentials(**regular_token)
    response = api_client.post("/api/news/", {
        "title": "Unauthorized News Creation",
        "content": "Regular users should not be able to create news.",
        "status": "draft",
    })
    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_delete_any_news(api_client, admin_token):
    another_user = User.objects.create_user(
        username="another_editor", password="password123")
    news = News.objects.create(
        title="Another Editor's News",
        content="Content",
        status="published",
        author=another_user
    )

    api_client.credentials(**admin_token)
    response = api_client.delete(f"/api/news/{news.id}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_admin_can_edit_any_news(api_client, admin_token):
    another_user = User.objects.create_user(
        username="another_editor", password="password123")
    news = News.objects.create(
        title="Another Editor's News",
        content="Content",
        status="published",
        author=another_user
    )

    api_client.credentials(**admin_token)
    response = api_client.patch(
        f"/api/news/{news.id}/", {"title": "Admin Edit"})
    assert response.status_code == 200
    assert response.data["title"] == "Admin Edit"


@pytest.mark.django_db
def test_regular_user_cannot_view_pro_news(api_client, regular_token):
    author = User.objects.create_user(
        username="news_author", password="password123")
    news = News.objects.create(
        title="Exclusive News for PRO",
        content="Only for PRO subscribers",
        status="published",
        is_pro_only=True,
        publication_date=timezone.now(),
        author=author
    )

    api_client.credentials(**regular_token)
    response = api_client.get(f"/api/news/{news.id}/")
    assert response.status_code == 403
