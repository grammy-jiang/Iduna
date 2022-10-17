"""
the serializer and viewset of Group model

* https://docs.djangoproject.com/en/4.1/topics/auth/default/#groups
"""
from django.contrib.auth.models import Group
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet


class GroupSerializer(ModelSerializer):
    """
    the serializer of Group model
    """

    class Meta:
        fields = "__all__"
        model = Group


class GroupViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    the viewset of Group model
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
