# Generated by Django 5.1.5 on 2025-03-29 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0018_cartitem_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payement_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
