"""
The utilities of admin
"""
import subprocess
from functools import wraps


def safe_check_output(func):
    """
    if subprocess.check_output raises CalledProcessError, return None instead
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except subprocess.CalledProcessError:
            return None

    return wrapper


class ReadOnlyAdminMixin:
    """
    The mixin for read-only admin
    """

    def has_add_permission(self, request):
        """
        Should return True if adding an object is permitted, False otherwise.
        :param request:
        :return:
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Should return True if editing obj is permitted, False otherwise. If obj is None,
        should return True or False to indicate whether editing of objects of this type
        is permitted in general (e.g., False will be interpreted as meaning that the
        current user is not permitted to edit any object of this type).
        :param request:
        :param obj:
        :return:
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Should return True if deleting obj is permitted, False otherwise. If obj is
        None, should return True or False to indicate whether deleting objects of this
        type is permitted in general (e.g., False will be interpreted as meaning that
        the current user is not permitted to delete any object of this type).
        :param request:
        :param obj:
        :return:
        """
        return False
