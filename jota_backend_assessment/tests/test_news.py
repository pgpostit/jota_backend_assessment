import pytest
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from news_api.models import News


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def editor_user(db):
    user = User.objects.create_user(username="editor", password="password123")
    editor_group, _ = Group.objects.get_or_create(name="Editor")
    user.groups.add(editor_group)
    return user


@pytest.fixture
def jwt_token(user):
    access_token = AccessToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


@pytest.fixture
def editor_token(editor_user):
    access_token = AccessToken.for_user(editor_user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


@pytest.mark.django_db
def test_create_news(api_client, editor_token):
    api_client.credentials(**editor_token)
    data = {
        "title": "New Article",
        "subtitle": "Subtitle",
        "content": "Article content.",
        "status": "draft",
    }
    response = api_client.post("/api/news/", data)
    assert response.status_code == 201
    assert response.data["title"] == data["title"]


@pytest.mark.django_db
def test_published_news_is_visible(api_client, editor_token, editor_user):
    news = News.objects.create(
        title="Public News",
        subtitle="Subtitle",
        content="News content.",
        status="published",
        author=editor_user
    )

    api_client.credentials(**editor_token)
    response = api_client.get(f"/api/news/{news.id}/")

    assert response.status_code == 200
    assert response.data["title"] == news.title
