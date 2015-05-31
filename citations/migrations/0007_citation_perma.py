# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citations', '0006_citation_webcite'),
    ]

    operations = [
        migrations.AddField(
            model_name='citation',
            name='perma',
            field=models.URLField(max_length=255, null=True),
        ),
    ]
