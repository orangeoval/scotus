# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citations', '0002_auto_20150427_0038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citation',
            name='redirected',
        ),
        migrations.RemoveField(
            model_name='citation',
            name='rotted',
        ),
        migrations.AddField(
            model_name='citation',
            name='status',
            field=models.CharField(default='a', max_length=1, choices=[('a', 'available'), ('u', 'unavailable'), ('r', 'redirected')]),
        ),
    ]
