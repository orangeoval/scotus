# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citations', '0003_auto_20150427_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citation',
            name='validated',
            field=models.URLField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='citation',
            name='verify_date',
            field=models.DateTimeField(null=True, verbose_name='date verified'),
        ),
    ]
