# -*- coding: utf-8 -*-

from scotus import settings
from django.utils import timezone
from django.db.models import Q

from discovery.Pdf import Pdf
from discovery.Pdf import Url
from opinions.models import Opinion
from citations.models import Citation
from justices.models import Justice

import lxml.html
from datetime import datetime


class Discovery:
    def __init__(self):
        self.discovered_opinions = []
        self.new_opinions = []
        self.category_urls = []
        self.pdfs_to_scrape = []
        self.BASE = 'http://www.supremecourt.gov'
        self.OPINIONS_BASE = self.BASE + '/opinions/'
        self.OPINIONS_MAIN_PAGE = self.OPINIONS_BASE + 'opinions.aspx'
        self.YYYYMMDD = timezone.now().strftime('%Y%m%d')

    def run(self):
        print '[INITATING DISCOVERY - %s]' % timezone.now()
        print '[**%s**]' % self.OPINIONS_MAIN_PAGE
        self.fetch_opinion_category_urls()
        self.get_opinions_from_categories()
        print '[INITIATING OPINION INGEST]'
        self.ingest_new_opinions()
        print '[INITIATION CITATION SCRAPING AND INGEST]'
        self.ingest_new_citations()
        print '[DISCOVERY COMPLETE]'

    def fetch_opinion_category_urls(self):
        request = Url.get(self.OPINIONS_MAIN_PAGE)

        if request and request.status_code == 200:
            html = lxml.html.fromstring(request.text)
            search = "//div[@class='panel-body dslist2']/ul/li/a/@href"
            for category in html.xpath(search):
                self.category_urls.append(self.OPINIONS_BASE + category)
            
    def get_opinions_from_categories(self):
        for category_url in self.category_urls:
            category = category_url.split('/')[-2]
            request = Url.get(category_url)    

            if request and request.status_code == 200:
                html = lxml.html.fromstring(request.text)
                search = "//table[@class='table table-bordered']/tr"

                for row in html.xpath(search):
                    opinion = []
                    for cell in row.xpath('./td'):
                        opinion.append(cell.text_content().strip())
                        for pdf_path in cell.xpath('./a/@href'):
                            opinion.append(self.BASE + pdf_path.strip())
                            
                    if opinion:
                        # Slip opinions have extra 'reporter' column as first
                        # column. Add blank first column to non slip opinions
                        if len(opinion) == 6:
                            opinion = [''] + opinion

                        # Standardize published date to YYYY-MM-DD format
                        opinion[1] = opinion[1].replace('-', '/')
                        opinion[1] = datetime.strptime(opinion[1], '%m/%d/%y').strftime('%Y-%m-%d')                

                        # Report out
                        print 'Discovered: %s  %s' % (opinion[3], opinion[4])

                        #TODO: email when new justice created so can create name on back end
                        if not Justice.objects.filter(id=opinion[5]):
                            justice = Justice(id=opinion[5], name=opinion[5])
                            justice.save()

                        self.discovered_opinions.append(Opinion(
                            category=category,
                            reporter=opinion[0],
                            published=opinion[1],
                            docket=opinion[2],
                            name=opinion[3],
                            pdf_url=opinion[4],
                            justice=Justice(opinion[5]),
                            part=opinion[6],
                            discovered=timezone.now(),
                        ))

    def ingest_new_opinions(self):

        # Sort opinions by publication date, oldest to newest
        self.discovered_opinions.sort(key=lambda o: o.published)

        for opinion in self.discovered_opinions:

            # If find match on all fields already in database, skip and continue
            if Opinion.objects.filter(
                name=opinion.name,
                pdf_url=opinion.pdf_url,
                published=opinion.published,
                category=opinion.category,
                reporter=opinion.reporter,
                docket=opinion.docket,
                justice=opinion.justice,
                part=opinion.part):

                print 'Skipping: %s' % opinion.name
                continue

            # Report out
            print 'Ingesting: %s  %s' % (opinion.name, opinion.pdf_url)

            # Check if opinion with different values but same name was previously published, set updated flag if so
            opinion.republished = False
            for prev in Opinion.objects.filter(name=opinion.name):
                prev.updated = True
                prev.save()
                opinion.republished = True

            if opinion.republished:
                print 'REPUBLISHED!: %s' % opinion.name

            # Ingest new opinion to database
            opinion.save()
            self.new_opinions.append(opinion)
            
    def ingest_new_citations(self):
        for opinion in self.new_opinions:
            local_pdf = settings.PDF_DIR + str(opinion.id) + '.pdf'
            opinion.pdf = Pdf(
                opinion.pdf_url,
                local_pdf,
            )

            print 'Downloading: %s  %s' % (opinion.name, opinion.pdf_url)
            opinion.pdf.download()
            print 'Scraping: %s  %s' % (opinion.name, local_pdf)
            opinion.pdf.scrape_urls()

            # Gather citations from previous publication of same opinion name, if they exist
            previous_check_list = []
            if opinion.republished:
                previous_citations = Citation.objects.filter(opinion__name=opinion.name).exclude(opinion_id=opinion.id)
                if previous_citations:
                   for previous in previous_citations:
                       previous_check_list.append(previous.scraped)
                       if previous.validated != '0':
                           previous_check_list.append(previous.validated)

            for url in opinion.pdf.urls:
                # Skip citation if scraped from of validated in previous discovery
                if url in previous_check_list:
                    print '--Skipping previously discovered citation for %s: %s' % (opinion.name, url)
                    continue
            
                print '++Ingesting citation: %s' % url

                # Check urls status, and see if archived
                status = self.check_url_status(url)

                new_citation = Citation(
                    opinion=Opinion(opinion.id),
                    scraped=url,
                    status=status[u'citation'],
                    archived_lc=status[u'archived_lc'],
                    archived_ia=status[u'archived_ia'],
                )
                new_citation.save()

    def check_url_status(self, url):
        status = {
            u'citation': u'a',
            u'archived_lc': False,
            u'archived_ia': False,
        }

        request = Url.get(url)
        if not request or request.status_code == 404:
            status[u'citation'] = u'u'
        if request and request.status_code in [302, 301]:
            status[u'citation'] = u'r'

        #TODO: Uncomment this on LIB network.  lx7 doesn't like machine requests off network
        #request = Url.get(Citation.WAYBACK_LC + url)
        #if request and request.status_code == 200:
        #    status[u'archived_lc'] = True

        request = Url.get(Citation.WAYBACK_IA + url)
        if request and request.status_code == 200:
            status[u'archived_ia'] = True

        return status

