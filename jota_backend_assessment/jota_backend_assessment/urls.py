from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from news_api.views import (
    CategoryViewSet,
    NewsViewSet,
    SubscriptionPlanViewSet,
    ReaderProfileViewSet,
)

schema_view = get_schema_view(
    openapi.Info(
        title="JOTA API",
        default_version="v1",
        description="API for news management",
    ),
    public=True,
    permission_classes=[AllowAny],
    authentication_classes=[],
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"news", NewsViewSet)
router.register(r"subscription-plans", SubscriptionPlanViewSet)
router.register(r"reader-profiles", ReaderProfileViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("swagger/", schema_view.with_ui("swagger",
         cache_timeout=0), name="schema-swagger-ui"),
]
