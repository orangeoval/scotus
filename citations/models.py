from django.db import models

class Citation(models.Model):
    GOOD_SCRAPE = 'gs'
    BAD_SCRAPE = 'bs'
    BAD_CITATION = 'bc'
    SCRAPE_EVALUATIONS = (
        (GOOD_SCRAPE, 'good scrape'),
        (BAD_SCRAPE, 'bad scrape'),
        (BAD_CITATION, 'bad citation'),
    )
    WAYBACKS = {
        'lc': 'http://webarchive.loc.gov/all/*/',
        'ia': 'http://web.archive.org/web/*/',
    }

    opinion = models.ForeignKey('opinions.Opinion')
    scraped = models.URLField(max_length=255)
    scrape_evaluation = models.CharField(max_length=2,
                                         choices=SCRAPE_EVALUATIONS,
                                         default=GOOD_SCRAPE)
    validated = models.URLField(max_length=255,default=0)
    verify_date = models.DateTimeField('date verified', blank=True, null=True)
    rotted = models.BooleanField(default=False)
    redirected = models.BooleanField(default=False)
    archived_lc = models.BooleanField(default=False)
    archives_ia = models.BooleanField(default=False)
