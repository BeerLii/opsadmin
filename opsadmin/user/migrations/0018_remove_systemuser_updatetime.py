# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 03:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_systemuser_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='systemuser',
            name='UpdateTime',
        ),
    ]
