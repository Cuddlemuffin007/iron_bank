# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-05 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iron_bank_app', '0005_auto_20160304_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.CharField(default='None', max_length=20),
        ),
    ]
