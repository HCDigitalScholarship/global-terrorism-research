# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-24 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtr_site', '0017_auto_20170722_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='context',
            name='keyword',
            field=models.ManyToManyField(to='gtr_site.Keyword'),
        ),
    ]
