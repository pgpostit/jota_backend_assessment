from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Q
from .models import Category, News, SubscriptionPlan, ReaderProfile
from .serializers import (
    CategorySerializer, NewsSerializer, SubscriptionPlanSerializer, ReaderProfileSerializer
)


class IsEditorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.user.groups.filter(name="Editor").exists():
            return obj.author == request.user
        return False


class CanCreateNews(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_superuser or request.user.groups.filter(name="Editor").exists()
        return True


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, CanCreateNews]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return News.objects.all()

        if user.groups.filter(name="Editor").exists():
            return News.objects.filter(Q(status="published") | Q(author=user))

        return News.objects.filter(status="published", publication_date__lte=timezone.now())

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if instance.is_pro_only:
            if not hasattr(user, "readerprofile") or user.readerprofile.plan.name != "JOTA PRO":
                raise PermissionDenied(
                    "This news article is exclusive to JOTA PRO subscribers.")

        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user

        if not user.is_superuser and not user.groups.filter(name="Editor").exists():
            raise PermissionDenied(
                "You do not have permission to create news articles.")

        serializer.save(author=user)

    def perform_update(self, serializer):
        user = self.request.user
        instance = serializer.instance

        if user.is_superuser:
            serializer.save()
            return

        if user.groups.filter(name="Editor").exists() and instance.author != user:
            raise PermissionDenied(
                "You do not have permission to edit this news article.")

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if user.is_superuser:
            instance.delete()
            return

        if user.groups.filter(name="Editor").exists() and instance.author != user:
            raise PermissionDenied(
                "You do not have permission to delete this news article.")

        instance.delete()

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def published(self, request):
        queryset = News.objects.filter(
            status="published", publication_date__lte=timezone.now())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAdminUser]


class ReaderProfileViewSet(viewsets.ModelViewSet):
    queryset = ReaderProfile.objects.all()
    serializer_class = ReaderProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
