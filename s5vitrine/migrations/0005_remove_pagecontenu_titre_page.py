# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-06 20:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('s5vitrine', '0004_auto_20161115_2139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagecontenu',
            name='titre_page',
        ),
    ]
