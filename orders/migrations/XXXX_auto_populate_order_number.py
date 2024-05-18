# orders/migrations/0008_auto_populate_order_number.py

from django.db import migrations, models
import uuid
from datetime import datetime

def populate_order_number(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    for order in Order.objects.all():
        if not order.order_number:
            today = datetime.today()
            date_str = today.strftime('%Y%m%d')
            unique_str = str(uuid.uuid4()).replace('-', '').upper()[:3]
            order.order_number = f"{date_str}-{unique_str}"
            order.save()

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),  # Ensure this points to the correct initial migration
    ]

    operations = [
        migrations.RunPython(populate_order_number),
    ]
