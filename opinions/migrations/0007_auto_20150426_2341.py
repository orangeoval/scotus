# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinions', '0006_opinion_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='category',
            field=models.CharField(max_length=30),
        ),
    ]
