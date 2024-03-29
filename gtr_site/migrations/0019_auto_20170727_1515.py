# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-27 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtr_site', '0018_auto_20170724_2010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyconpairs',
            name='context_in_pair',
        ),
        migrations.RemoveField(
            model_name='keyconpairs',
            name='keyword_in_pair',
        ),
        migrations.RemoveField(
            model_name='keyconpairs',
            name='statement',
        ),
        migrations.RemoveField(
            model_name='statement',
            name='full_text',
        ),
        migrations.RemoveField(
            model_name='statement',
            name='statement_contexts',
        ),
        migrations.RemoveField(
            model_name='statement',
            name='statement_keywords',
        ),
        migrations.AddField(
            model_name='context',
            name='statement',
            field=models.ManyToManyField(to='gtr_site.Statement'),
        ),
        migrations.AddField(
            model_name='keyword',
            name='statement',
            field=models.ManyToManyField(to='gtr_site.Statement'),
        ),
        migrations.AddField(
            model_name='statement',
            name='access',
            field=models.CharField(choices=[('AL', 'All Users'), ('HC', 'Haverford Users only')], default='AL', max_length=2),
        ),
        migrations.DeleteModel(
            name='KeyConPairs',
        ),
    ]
