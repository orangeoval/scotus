# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinions', '0003_auto_20150424_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='published',
            field=models.DateField(verbose_name=b'date published'),
        ),
    ]
