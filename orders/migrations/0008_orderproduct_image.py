# Generated by Django 5.0.1 on 2024-06-06 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_zip'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='image',
            field=models.ImageField(default=2, upload_to='photos/products'),
            preserve_default=False,
        ),
    ]