# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinions', '0002_opinion_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='reporter',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
