# Generated by Django 5.1.5 on 2025-03-07 17:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0010_remove_order_garment_alter_order_measurements_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.product')),
            ],
        ),
    ]
