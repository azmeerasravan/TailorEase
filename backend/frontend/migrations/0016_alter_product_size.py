# Generated by Django 5.1.5 on 2025-03-29 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0015_remove_product_fabric_product_fabric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
