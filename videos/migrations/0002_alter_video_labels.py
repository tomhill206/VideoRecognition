# Generated by Django 4.2.3 on 2023-07-25 15:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("videos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="labels",
            field=models.JSONField(null=True),
        ),
    ]
