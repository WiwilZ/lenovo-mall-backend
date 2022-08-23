# Generated by Django 4.1 on 2022-08-22 17:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ReceivingAddress",
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
                ("consignee", models.CharField(max_length=128)),
                ("address", models.CharField(max_length=128)),
                ("phone_number", models.CharField(max_length=128)),
                ("is_default", models.BooleanField(default=False)),
                (
                    "related_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="receiving_addresses",
                        related_query_name="receiving_address",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
