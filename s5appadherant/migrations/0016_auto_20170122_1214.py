# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-22 12:14
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('s5appadherant', '0015_auto_20170122_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variete',
            name='description',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
