# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citations', '0005_auto_20150518_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='citation',
            name='webcite',
            field=models.URLField(max_length=255, null=True),
        ),
    ]
