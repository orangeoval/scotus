# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinions', '0007_auto_20150426_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='category',
            field=models.CharField(max_length=100),
        ),
    ]
