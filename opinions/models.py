# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from justices.models import Justice
from citations.models import Citation

class Opinion(models.Model):

    category = models.CharField(max_length=30)
    discovered = models.DateTimeField('date discovered')
    published = models.DateField('date published')
    name = models.CharField(max_length=255)
    pdf_url = models.URLField(max_length=255)
    reporter = models.CharField(max_length=50, blank=True, null=True)
    docket = models.CharField(max_length=20)
    part = models.CharField(max_length=20)
    justice = models.ForeignKey('justices.Justice'); 
    updated = models.BooleanField(default=False)

    def get_counts_and_update_date(self):
        self.citation_count = Citation.objects.filter(opinion=self.id).count()

        if self.updated:
            self.updated_date = Opinion.objects.filter(name=self.name).latest('published').published
        else:
            self.updated_date = False
