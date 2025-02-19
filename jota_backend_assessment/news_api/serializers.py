from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, News, SubscriptionPlan, ReaderProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True)

    class Meta:
        model = News
        fields = [
            "id", "title", "subtitle", "image", "content", "publication_date",
            "author", "status", "category", "is_pro_only", "created_date", "updated_date"
        ]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True)

    class Meta:
        model = SubscriptionPlan
        fields = ["id", "name", "categories"]


class ReaderProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ReaderProfile
        fields = ["id", "user", "plan"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
