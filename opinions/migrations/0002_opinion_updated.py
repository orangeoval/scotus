# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='updated',
            field=models.DateTimeField(null=True, verbose_name=b'date updated', blank=True),
        ),
    ]
