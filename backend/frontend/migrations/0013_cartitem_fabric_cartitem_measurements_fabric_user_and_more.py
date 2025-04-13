# Generated by Django 5.1.5 on 2025-03-27 16:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0012_alter_userprofile_address_alter_userprofile_contact_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='fabric',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.fabric'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='measurements',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='fabric',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='fabric',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.fabric'),
        ),
    ]
