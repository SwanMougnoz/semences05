# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-22 19:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s5appadherant', '0017_auto_20170122_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jardin',
            name='short_description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'R\xc3\xa9sum\xc3\xa9'),
        ),
        migrations.AlterField(
            model_name='variete',
            name='short_description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'R\xc3\xa9sum\xc3\xa9'),
        ),
    ]
