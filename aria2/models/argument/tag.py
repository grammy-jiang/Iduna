from django.db import models


class ArgumentTag(models.Model):
    """
    The model of Aria2 Argument Tag
    """

    value = models.CharField(max_length=256, primary_key=True, unique=True)

    class Meta:
        verbose_name = "Aria2c - Argument Tag"

    def __str__(self) -> str:
        """

        :return:
        :rtype: str
        """
        return self.value
