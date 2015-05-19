# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citations', '0004_auto_20150430_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citation',
            name='archived_ia',
        ),
        migrations.RemoveField(
            model_name='citation',
            name='archived_lc',
        ),
        migrations.AddField(
            model_name='citation',
            name='memento',
            field=models.URLField(max_length=255, null=True),
        ),
    ]
