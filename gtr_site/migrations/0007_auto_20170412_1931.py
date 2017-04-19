# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtr_site', '0006_auto_20170412_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='issue_date',
            field=models.DateField(),
        ),
    ]
