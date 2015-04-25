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

    def verify_ingest(self, dictionary=False):
        if not dictionary:
            return False

        for key in Opinion.REQUIRED_KEYS:
            if not key in dictionary:
                return False
            else:
                if key == 'justice':
                    dictionary[key] = Justice(dictionary[key])

                setattr(self, key, dictionary[key])

        if Opinion.objects.filter(
            name=self.name,
            pdf_url=self.pdf_url,
            published=self.published,
            category=self.category,
            reporter=self.reporter,
            docket=self.docket,
            justice=self.justice,
            part=self.part,):

            return False

        self.discovered = timezone.now()
        return True

    def ingest(self):
        self.save()
