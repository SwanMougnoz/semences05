# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-06 20:34
from __future__ import unicode_literals

from django.db import migrations, models
import s5appadherant.models.variete


class Migration(migrations.Migration):

    dependencies = [
        ('s5appadherant', '0004_auto_20161127_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variete',
            name='photo',
            field=models.ImageField(null=True, upload_to=s5appadherant.models.variete.get_variete_upload_path),
        ),
    ]
