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

    REQUIRED_KEYS = [
        'category',
        'reporter',
        'published',
        'docket',
        'name',
        'pdf_url',
        'justice',
        'part',
    ]

    def verify_dictionary(self, dictionary=False):
        if not dictionary:
            self.is_valid = False
            self.can_ingest = False
        if dictionary:
            self.is_valid = True
            self.can_ingest = True

            for key in Opinion.REQUIRED_KEYS:
                if not key in dictionary:
                    self.is_valid = False
                else:
                    if key == 'justice':
                        dictionary[key] = Justice(dictionary[key])
                    setattr(self, key, dictionary[key])
            if self.is_valid:
                if Opinion.objects.filter(name=dictionary['name'],pdf_url=dictionary['pdf_url']):
                    self.can_ingest = False

    def ingest(self, dictionary):
        if not Opinion.objects.filter(name=dictionary['name']):
            self.category = dictionary['category']
            self.reporter = dictionary['reporter']
            self.published = dictionary['published']
            self.docket = dictionary['docket']
            self.name = dictionary['name']
            self.pdf_url = dictionary['pdf_url']
            self.justice = Justice(dictionary['justice'])
            self.part = dictionary['part']
            self.discovered = timezone.now()
