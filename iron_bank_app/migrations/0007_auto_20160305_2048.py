# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-05 20:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iron_bank_app', '0006_auto_20160305_1948'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-post_date']},
        ),
    ]
