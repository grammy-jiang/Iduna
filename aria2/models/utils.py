"""
the utilities
"""
from django.db import models


class TimeStampMixin(models.Model):
    """
    a mixin to record created and updated timestamp
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
