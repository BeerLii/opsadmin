# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-04 09:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0007_auto_20171202_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpu',
            name='asset',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cpu_asset', to='asset.Asset'),
        ),
        migrations.AlterField(
            model_name='disk',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disk_asset', to='asset.Asset'),
        ),
        migrations.AlterField(
            model_name='nic',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nic_asset', to='asset.Asset'),
        ),
        migrations.AlterField(
            model_name='ram',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ram_asset', to='asset.Asset'),
        ),
    ]
