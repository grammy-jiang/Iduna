# Generated by Django 4.1.2 on 2022-10-24 02:11

import django.db.models.deletion
from django.db import migrations, models

import aria2.models.aria2c


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("aria2", "0020_initial_profile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Aria2cInstance",
            fields=[
                ("pid", models.IntegerField(primary_key=True, serialize=False)),
                ("command", models.CharField(max_length=256, unique=True)),
                (
                    "aria2c",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="aria2.aria2c"
                    ),
                ),
                (
                    "profile",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="aria2.aria2cprofile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Aria2c - Instance",
            },
        ),
    ]