from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    NewsViewSet,
    SubscriptionPlanViewSet,
    ReaderProfileViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"news", NewsViewSet)
router.register(r"subscription-plans", SubscriptionPlanViewSet)
router.register(r"reader-profiles", ReaderProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
