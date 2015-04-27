from django.db import models

class Citation(models.Model):
    SCRAPE_EVALUATIONS = (
        (u'gs', u'good scrape'),
        (u'bs', u'bad scrape'),
        (u'bc', u'bad citation'),
    )
    STATUSES = (
        (u'a', u'available'),
        (u'u', u'unavailable'),
        (u'r', u'redirected'),
    )
    WAYBACKS = {
        'lc': 'http://webarchive.loc.gov/all/*/',
        'ia': 'http://web.archive.org/web/*/',
    }

    opinion = models.ForeignKey('opinions.Opinion')
    scraped = models.URLField(max_length=255)
    scrape_evaluation = models.CharField(max_length=2,
                                         choices=SCRAPE_EVALUATIONS,
                                         default=u'gs')
    status = models.CharField(max_length=1,
                              choices=STATUSES,
                              default=u'a')
    validated = models.URLField(max_length=255,default=0)
    verify_date = models.DateTimeField(u'date verified', blank=True, null=True)
    archived_lc = models.BooleanField(default=False)
    archived_ia = models.BooleanField(default=False)
