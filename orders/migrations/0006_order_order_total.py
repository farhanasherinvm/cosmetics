# Generated by Django 5.0.1 on 2024-05-22 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_merge_0004_order_ip_XXXX_auto_populate_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_total',
            field=models.FloatField(default=0.0),
        ),
    ]
