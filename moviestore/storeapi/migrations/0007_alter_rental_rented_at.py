# Generated by Django 4.0 on 2021-12-26 13:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('storeapi', '0006_alter_rental_rented_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='rented_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 26, 13, 32, 58, 206354, tzinfo=utc)),
        ),
    ]