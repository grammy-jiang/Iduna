# Generated by Django 4.1.2 on 2022-10-24 02:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aria2", "0010_initial_aria2c"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArgumentPair",
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
                ("value", models.CharField(max_length=256)),
                (
                    "argument",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="aria2.argument",
                    ),
                ),
            ],
            options={
                "verbose_name": "Aria2c - Argument Pair",
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "name",
                    models.CharField(max_length=256, primary_key=True, serialize=False),
                ),
                (
                    "arguments",
                    models.ManyToManyField(
                        through="aria2.ArgumentPair", to="aria2.argument"
                    ),
                ),
                (
                    "binary",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="aria2.Binary"
                    ),
                ),
                (
                    "args",
                    models.CharField(
                        blank=True, max_length=256, null=True, unique=True
                    ),
                ),
            ],
            options={
                "verbose_name": "Aria2c - Profile",
            },
        ),
        migrations.AddField(
            model_name="argumentpair",
            name="profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="aria2.profile"
            ),
        ),
        migrations.AddConstraint(
            model_name="argumentpair",
            constraint=models.UniqueConstraint(
                fields=("profile", "argument"), name="unique_argument_pair"
            ),
        ),
    ]
