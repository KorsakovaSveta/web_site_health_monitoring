# Generated by Django 5.0 on 2023-12-22 03:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0002_physicalindicators_fitnessbracelet"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fitnessbracelet",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="physicalindicators",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
