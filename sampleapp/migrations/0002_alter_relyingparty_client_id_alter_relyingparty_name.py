# Generated by Django 4.2.17 on 2024-12-29 01:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sampleapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="relyingparty",
            name="client_id",
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name="relyingparty",
            name="name",
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
