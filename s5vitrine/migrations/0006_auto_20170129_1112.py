# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-29 11:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s5vitrine', '0005_remove_pagecontenu_titre_page'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menuitem',
            options={'verbose_name': 'Menu', 'verbose_name_plural': 'Liens du menu'},
        ),
        migrations.AlterModelOptions(
            name='pagecontenu',
            options={'verbose_name': 'Page de contenu', 'verbose_name_plural': 'Pages de contenu'},
        ),
        migrations.AlterModelOptions(
            name='pagegenerique',
            options={'verbose_name': 'Page sp\xe9ciale', 'verbose_name_plural': 'Pages sp\xe9ciales'},
        ),
        migrations.AddField(
            model_name='pagegenerique',
            name='name',
            field=models.CharField(default=b'special_page', max_length=255),
        ),
        migrations.RunSQL("update s5vitrine_pagegenerique set name='Accueil' where viewname='s5vitrine:accueil'"),
        migrations.RunSQL("update s5vitrine_pagegenerique set name='Contact' where viewname='s5vitrine:contact'"),
        migrations.RunSQL("update s5vitrine_pagegenerique set name='Variétés' where viewname='s5vitrine:variete_list'")
    ]

