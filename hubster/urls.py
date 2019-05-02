from django.urls import include, path
from rest_framework import routers

from hubster import views

router = routers.DefaultRouter()
router.register(r"users", views.GithubUserViewSet)

urlpatterns = [path("", include(router.urls))]
