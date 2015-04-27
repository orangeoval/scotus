# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citation',
            old_name='archives_ia',
            new_name='archived_ia',
        ),
    ]
