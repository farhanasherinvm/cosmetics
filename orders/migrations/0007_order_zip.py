# Generated by Django 5.0.1 on 2024-06-06 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='zip',
            field=models.BigIntegerField(default='00000', max_length=6),
        ),
    ]