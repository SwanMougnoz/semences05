# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-27 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s5appadherant', '0002_auto_20161127_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variete',
            name='photo',
            field=models.ImageField(upload_to=b'varietes'),
        ),
    ]