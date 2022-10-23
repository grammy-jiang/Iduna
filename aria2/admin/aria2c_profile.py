"""
The admin of Aria2 Profile model of aria2
"""

from django.contrib import admin

from ..models import ArgumentPair, Aria2cProfile


@admin.register(ArgumentPair)
class ArgumentPairAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 Argument Pair model of aria2
    """

    list_display = ("profile", "argument", "value")


class ArgumentPairInline(admin.TabularInline):
    """
    The inline of Argument Pair
    """

    model = ArgumentPair
    ordering = ("argument",)


@admin.register(Aria2cProfile)
class Aria2cProfileAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 Profile model of aria2
    """

    inlines = (ArgumentPairInline,)
