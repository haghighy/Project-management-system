# Generated by Django 5.1.5 on 2025-02-03 07:22

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Board",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("is_public", models.BooleanField(default=False)),
                ("is_closed", models.BooleanField(default=False)),
                ("date_closed", models.DateTimeField(blank=True, null=True)),
                ("date_last_view", models.DateTimeField(auto_now=True)),
                ("date_last_activity", models.DateTimeField(auto_now=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("shared_link", models.URLField(blank=True, null=True)),
                (
                    "member_creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_boards",
                        to="accounts.member",
                    ),
                ),
            ],
        ),
    ]
