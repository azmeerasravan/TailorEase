# Generated by Django 5.1.5 on 2025-01-30 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('customer', 'Customer'), ('vendor', 'Vendor')], default='customer', max_length=50),
        ),
    ]
