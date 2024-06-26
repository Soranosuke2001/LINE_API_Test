# Generated by Django 5.0.6 on 2024-06-28 03:45

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LineImage",
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
                ("image_url", models.CharField(max_length=256)),
                ("content_provider", models.CharField(max_length=10)),
                ("source_type", models.CharField(max_length=10)),
                ("reply_token", models.CharField(max_length=100)),
                ("is_redelivery", models.BooleanField()),
                ("user_id", models.CharField(max_length=256)),
                ("webhook_event_id", models.CharField(max_length=256)),
                ("timestamp", models.DateTimeField()),
                ("received_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
