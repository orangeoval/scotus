from django.db import models
from django.utils import timezone
from justices.models import Justice

class Opinion(models.Model):

    category = models.CharField(max_length=15)
    discovered = models.DateTimeField('date discovered')
    published = models.DateField('date published')
    name = models.CharField(max_length=255)
    pdf_url = models.URLField(max_length=255)
    reporter = models.CharField(max_length=50, blank=True, null=True)
    docket = models.CharField(max_length=20)
    part = models.CharField(max_length=20)
    justice = models.ForeignKey('justices.Justice'); 
    updated = models.BooleanField(default=False)
