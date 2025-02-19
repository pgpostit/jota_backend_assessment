import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from news_api.models import News, SubscriptionPlan, ReaderProfile
from django.utils import timezone


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def subscription_basic(db):
    return SubscriptionPlan.objects.get_or_create(name="BASIC")[0]


@pytest.fixture
def subscription_pro(db):
    return SubscriptionPlan.objects.get_or_create(name="JOTA PRO")[0]


@pytest.fixture
def reader_user(db, subscription_basic):
    user = User.objects.create_user(username="reader", password="password123")
    ReaderProfile.objects.create(user=user, plan=subscription_basic)
    return user


@pytest.fixture
def reader_pro_user(db, subscription_pro):
    user = User.objects.create_user(
        username="reader_pro", password="password123")
    ReaderProfile.objects.create(user=user, plan=subscription_pro)
    return user


@pytest.fixture
def reader_token(reader_user):
    access_token = AccessToken.for_user(reader_user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


@pytest.fixture
def reader_pro_token(reader_pro_user):
    access_token = AccessToken.for_user(reader_pro_user)
    return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}


@pytest.mark.django_db
def test_reader_can_view_public_news(api_client, reader_token, reader_user):
    news = News.objects.create(
        title="Public News",
        subtitle="Subtitle",
        content="Public content",
        status="published",
        author=reader_user,
        publication_date=timezone.now(),
        is_pro_only=False
    )

    api_client.credentials(**reader_token)
    response = api_client.get(f"/api/news/{news.id}/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_reader_cannot_view_pro_news(api_client, reader_token, reader_user):
    news = News.objects.create(
        title="Pro Exclusive News",
        subtitle="Subtitle",
        content="Pro content",
        status="published",
        author=reader_user,
        publication_date=timezone.now(),
        is_pro_only=True
    )

    api_client.credentials(**reader_token)
    response = api_client.get(f"/api/news/{news.id}/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_reader_pro_can_view_pro_news(api_client, reader_pro_token, reader_pro_user):
    news = News.objects.create(
        title="Pro News",
        subtitle="Subtitle",
        content="Exclusive content for PRO users",
        status="published",
        author=reader_pro_user,
        publication_date=timezone.now(),
        is_pro_only=True
    )

    api_client.credentials(**reader_pro_token)
    response = api_client.get(f"/api/news/{news.id}/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_reader_cannot_create_news(api_client, reader_token):
    api_client.credentials(**reader_token)
    response = api_client.post(
        "/api/news/", {"title": "New Article", "content": "Content"})
    assert response.status_code == 403
