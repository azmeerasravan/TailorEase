# Generated by Django 5.1.5 on 2025-03-29 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0019_order_payement_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payement_id',
            new_name='payment_id',
        ),
    ]
