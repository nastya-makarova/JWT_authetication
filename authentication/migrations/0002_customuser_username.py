# Generated by Django 5.1.5 on 2025-01-18 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="username",
            field=models.CharField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
