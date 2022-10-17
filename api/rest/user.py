"""
the serializer and viewset of User model
"""
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

User = get_user_model()


class UserSerializer(ModelSerializer):
    """
    the serializer of User model
    """

    class Meta:
        fields = "__all__"
        model = User


class UserViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    the viewset of User model
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
