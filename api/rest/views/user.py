"""
the viewset of User model
"""
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from ..serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    the viewset of User model
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
