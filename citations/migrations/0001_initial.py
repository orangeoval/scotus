# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Citation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scraped', models.URLField(max_length=255)),
                ('scrape_evaluation', models.CharField(default=b'gs', max_length=2, choices=[(b'gs', b'good scrape'), (b'bs', b'bad scrape'), (b'bc', b'bad citation')])),
                ('validated', models.URLField(default=0, max_length=255)),
                ('verify_date', models.DateTimeField(null=True, verbose_name=b'date verified', blank=True)),
                ('rotted', models.BooleanField(default=False)),
                ('redirected', models.BooleanField(default=False)),
                ('archived_lc', models.BooleanField(default=False)),
                ('archives_ia', models.BooleanField(default=False)),
                ('opinion', models.ForeignKey(to='opinions.Opinion')),
            ],
        ),
    ]
