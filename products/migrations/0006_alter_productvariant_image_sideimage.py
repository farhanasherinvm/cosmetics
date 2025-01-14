# Generated by Django 5.0.1 on 2025-01-14 18:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_productvariant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/variants'),
        ),
        migrations.CreateModel(
            name='SideImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/side_images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='side_images', to='products.product')),
            ],
        ),
    ]
