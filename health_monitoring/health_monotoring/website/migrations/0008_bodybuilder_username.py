# Generated by Django 5.0 on 2024-01-01 19:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0007_alter_bodybuilder_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="bodybuilder",
            name="username",
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
