# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-01-26 16:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gtr_site', '0032_auto_20171108_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(blank=True, max_length=200)),
                ('statements', models.ManyToManyField(blank=True, to='gtr_site.Statement')),
                ('user', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
       ),
    ]
