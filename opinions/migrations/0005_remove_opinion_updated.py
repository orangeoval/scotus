# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinions', '0004_auto_20150425_0948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opinion',
            name='updated',
        ),
    ]
