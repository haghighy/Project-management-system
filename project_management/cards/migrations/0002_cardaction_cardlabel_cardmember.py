# Generated by Django 5.1.5 on 2025-02-03 07:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("board", "0002_boardaction_boardlabel_boardmember"),
        ("cards", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CardAction",
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
                ("data", models.JSONField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("action_type", models.CharField(max_length=50)),
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="actions",
                        to="cards.card",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.member",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CardLabel",
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
                (
                    "board_label",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="board.boardlabel",
                    ),
                ),
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="labels",
                        to="cards.card",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CardMember",
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
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="members",
                        to="cards.card",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.member",
                    ),
                ),
            ],
        ),
    ]
