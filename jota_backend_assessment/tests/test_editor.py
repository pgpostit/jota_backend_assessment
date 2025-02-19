import pytest
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from news_api.models import News


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def editor_user(db):
    user = User.objects.create_user(username="editor", password="password123")
    editor_group, _ = Group.objects.get_or_create(name="Editor")
    user.groups.add(editor_group)
    return user


@pytest.fixture
def editor_token(editor_user):
    access_token = AccessToken.for_user(editor_user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


@pytest.mark.django_db
def test_editor_can_create_news(api_client, editor_token):
    api_client.credentials(**editor_token)
    response = api_client.post(
        "/api/news/",
        {"title": "Editor News", "content": "News content", "status": "draft"},
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_editor_can_edit_own_news(api_client, editor_token, editor_user):
    news = News.objects.create(
        title="Original Title", content="Content", status="draft", author=editor_user
    )
    api_client.credentials(**editor_token)
    response = api_client.patch(
        f"/api/news/{news.id}/", {"title": "Updated Title"})
    assert response.status_code == 200
    assert response.data["title"] == "Updated Title"


@pytest.mark.django_db
def test_editor_cannot_edit_other_users_news(api_client, editor_token):
    other_user = User.objects.create_user(
        username="other_editor", password="password123")
    news = News.objects.create(
        title="Other's News", content="Content", status="published", author=other_user
    )
    api_client.credentials(**editor_token)
    response = api_client.patch(
        f"/api/news/{news.id}/", {"title": "Illegal Edit"})
    assert response.status_code == 403


@pytest.mark.django_db
def test_editor_can_view_all_news(api_client, editor_token):
    response = api_client.get("/api/news/", **editor_token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_editor_cannot_delete_other_users_news(api_client, editor_token):
    other_user = User.objects.create_user(
        username="other_editor", password="password123")
    news = News.objects.create(
        title="Other's News", content="Content", status="published", author=other_user
    )
    api_client.credentials(**editor_token)
    response = api_client.delete(f"/api/news/{news.id}/")
    assert response.status_code == 403
