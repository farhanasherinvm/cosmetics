# Generated by Django 5.0.1 on 2024-05-02 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_address_zip'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='new_user',
            new_name='new_name',
        ),
    ]