# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-27 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s5appadherant', '0003_auto_20161127_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variete',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='variete',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'varietes'),
        ),
    ]
