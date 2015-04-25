# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinions', '0005_remove_opinion_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='updated',
            field=models.BooleanField(default=False),
        ),
    ]
