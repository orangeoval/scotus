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
    WAYBACK_LC = 'http://webarchive.loc.gov/all/*/'
    WAYBACK_IA = 'http://web.archive.org/web/*/'

    opinion = models.ForeignKey('opinions.Opinion')
    scraped = models.URLField(max_length=255)
    scrape_evaluation = models.CharField(
        max_length=2,
        choices=SCRAPE_EVALUATIONS,
        default=u'gs'
    )
    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=u'a'
    )
    validated = models.URLField(max_length=255, null=True)
    verify_date = models.DateTimeField(u'date verified', null=True)
    archived_lc = models.BooleanField(default=False)
    archived_ia = models.BooleanField(default=False)

    def set_status(self, status):
        for key in status:
            setattr(self, key, status[key])

    def csv_row(self):
        ST = Citation.STATUSES
        st = self.status
        SE = Citation.SCRAPE_EVALUATIONS
        se = self.scrape_evaluation

        self.st = [x[1] for x in ST if x[0] == st][0]
        self.se = [x[1] for x in SE if x[0] == se][0]
        

        for attr in self.__dict__:
            if attr == 'opinion' or attr.startswith('_'):
                continue

            data = getattr(self, attr)

            if data is None:
                data = ''
            elif not type(data) in [str, unicode]:
                data = str(data)

            setattr(self, attr, data.encode('utf8'))

        self.opinion.name = self.opinion.name.encode('utf8')
        self.opinion.justice.name = self.opinion.justice.name.encode('utf8')
        self.opinion.category = self.opinion.category.encode('utf8')
        self.opinion.published = self.opinion.published.strftime('%Y-%m-%d').encode('utf8')
        self.opinion.discovered = self.opinion.discovered.strftime('%Y-%m-%d').encode('utf8')
        self.opinion.pdf_url = self.opinion.pdf_url.encode('utf8')
        self.opinion.reporter = self.opinion.reporter.encode('utf8')
        self.opinion.docket = self.opinion.docket.encode('utf8')
        self.opinion.part = self.opinion.part.encode('utf8')
        

        return [
            self.scraped,
            self.validated,
            self.verify_date,
            self.se,
            self.st,
            self.archived_lc,
            self.archived_ia,
            self.opinion.name,
            self.opinion.justice.name,
            self.opinion.category,
            self.opinion.published,
            self.opinion.discovered,
            self.opinion.pdf_url,
            self.opinion.reporter,
            self.opinion.docket,
            self.opinion.part,
        ]
