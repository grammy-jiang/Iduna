"""
the serializer of User model
"""
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserSerializer(ModelSerializer):
    """
    the serializer of User model
    """

    class Meta:
        fields = "__all__"
        model = User
