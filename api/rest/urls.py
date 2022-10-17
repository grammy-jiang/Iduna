"""
REST framework adds support for automatic URL routing to Django, and provides you with a
simple, quick and consistent way of wiring your view logic to a set of URLs.

* https://www.django-rest-framework.org/api-guide/routers/
"""
from django.urls import include, path
from rest_framework import routers

from .user import UserViewSet

router = routers.DefaultRouter()
router.register("users", viewset=UserViewSet, basename="user")

urlpatterns = [path("", include(router.urls))]
