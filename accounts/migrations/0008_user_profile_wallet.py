# Generated by Django 5.0.1 on 2024-06-04 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_address_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='wallet',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
