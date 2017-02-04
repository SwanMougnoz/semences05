# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-28 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actstream', '0002_remove_action_data'),
        ('s5appadherant', '0020_cultivateur_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='adherant',
            name='processed_actions',
            field=models.ManyToManyField(related_name='adherant_has_proceed', to='actstream.Action'),
        ),
        migrations.DeleteModel(
            name='ProcessedAction',
        ),
    ]
