# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtr_site', '0005_auto_20170321_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='issue_date',
            field=models.DateTimeField(),
        ),
    ]
