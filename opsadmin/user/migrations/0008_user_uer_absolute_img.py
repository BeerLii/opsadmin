# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-15 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_user_user_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uer_absolute_img',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
