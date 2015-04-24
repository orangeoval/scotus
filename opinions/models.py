from django.db import models

class Opinion(models.Model):
    OPINIONS_PAGE = 'http://www.supremecourt.gov/opinions/opinions.aspx'

    category = models.CharField(max_length=15)
    discovered = models.DateTimeField('date discovered')
    published = models.DateTimeField('date published')
    name = models.CharField(max_length=255)
    pdf_url = models.URLField(max_length=255)
    reporter = models.CharField(max_length=50)
    docket = models.CharField(max_length=20)
    part = models.CharField(max_length=20)
    justice = models.ForeignKey('justices.Justice'); 
