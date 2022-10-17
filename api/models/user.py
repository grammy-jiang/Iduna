"""
If you’re starting a new project, it’s highly recommended to set up a custom user model,
even if the default User model is sufficient for you.

* https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
"""
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    This model behaves identically to the default user model, but it will be easy to
    be customized in the future if the need arises
    """
