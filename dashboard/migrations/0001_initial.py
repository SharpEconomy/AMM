# Generated by Django 5.2.4 on 2025-07-23 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OpportunityLog",
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
                ("timestamp", models.DateTimeField()),
                ("delta_percent", models.FloatField()),
                ("uniswap_price", models.FloatField()),
                ("average_price", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="PriceSnapshot",
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
                ("timestamp", models.DateTimeField()),
                ("uniswap_price", models.FloatField()),
                ("bitmart_price", models.FloatField(blank=True, null=True)),
                ("coinstore_price", models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
