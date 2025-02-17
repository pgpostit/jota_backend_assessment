from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    CATEGORIES = [
        ("poder", "Poder"),
        ("tributos", "Tributos"),
        ("saude", "Saúde"),
        ("energia", "Energia"),
        ("trabalhista", "Trabalhista"),
    ]

    name = models.CharField(max_length=50, choices=CATEGORIES, unique=True)

    def __str__(self):
        return self.name


class News(BaseModel):
    STATUS_OPTIONS = [
        ("draft", "Rascunho"),
        ("published", "Publicado"),
    ]

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to="news_images/", blank=True, null=True)
    content = models.TextField()
    publication_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=STATUS_OPTIONS, default="draft")
    category = models.ManyToManyField(Category)
    is_pro_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class SubscriptionPlan(BaseModel):
    PLAN_OPTIONS = [
        ("JOTA Info", "JOTA Info"),
        ("JOTA PRO", "JOTA PRO"),
    ]

    name = models.CharField(max_length=20, choices=PLAN_OPTIONS, unique=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class ReaderProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
