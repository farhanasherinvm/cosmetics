# Generated by Django 5.0.1 on 2024-03-21 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
