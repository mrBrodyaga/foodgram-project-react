# Generated by Django 3.1 on 2021-09-18 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_auto_20210805_1849"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="shoppingcart",
            name="amount",
        ),
    ]
