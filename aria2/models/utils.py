"""
the utilities
"""
from django.db import models


class TimeStampMixin(models.Model):
    """
    a mixin to record created and updated timestamp
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
