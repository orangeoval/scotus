# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citations', '0007_citation_perma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citation',
            name='status',
            field=models.CharField(default='a', max_length=1, choices=[('a', 'available'), ('u', 'unavailable'), ('r', 'redirect')]),
        ),
    ]
