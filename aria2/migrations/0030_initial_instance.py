# Generated by Django 4.1.2 on 2022-10-24 02:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("aria2", "0020_initial_profile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Instance",
            fields=[
                ("pid", models.IntegerField(primary_key=True, serialize=False)),
                ("command", models.CharField(max_length=256, unique=True)),
                (
                    "binary",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="aria2.Binary"
                    ),
                ),
                (
                    "profile",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="aria2.profile",
                    ),
                ),
                (
                    "effective_user_name",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "session_id",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "verbose_version",
                    models.CharField(blank=True, max_length=1024, null=True),
                ),
                (
                    "version",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
            ],
            options={
                "verbose_name": "Aria2c - Instance",
            },
        ),
    ]
