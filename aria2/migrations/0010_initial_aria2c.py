# Generated by Django 4.1.2 on 2022-10-24 02:11

import django.db.models.deletion
from django.db import migrations, models

import aria2.models.binary


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Binary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("path", aria2.models.binary.PathField(max_length=256)),
            ],
            options={
                "verbose_name": "Aria2c - Binary",
                "verbose_name_plural": "Aria2c - Binaries",
            },
        ),
        migrations.CreateModel(
            name="Aria2cArgumentTag",
            fields=[
                (
                    "value",
                    models.CharField(
                        max_length=256, primary_key=True, serialize=False, unique=True
                    ),
                ),
            ],
            options={
                "verbose_name": "Aria2c - Argument Tag",
            },
        ),
        migrations.CreateModel(
            name="Aria2cArgument",
            fields=[
                (
                    "short_argument",
                    models.CharField(
                        blank=True, max_length=256, null=True, unique=True
                    ),
                ),
                (
                    "long_argument",
                    models.CharField(max_length=256, primary_key=True, serialize=False),
                ),
                ("description", models.CharField(max_length=256)),
                (
                    "possible_values",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ("default", models.CharField(blank=True, max_length=256, null=True)),
                (
                    "aria2c",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="aria2.Binary"
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(to="aria2.aria2cargumenttag"),
                ),
            ],
            options={
                "verbose_name": "Aria2c - Argument",
            },
        ),
    ]
