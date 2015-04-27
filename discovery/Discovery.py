# -*- coding: utf-8 -*-

from scotus import settings
from django.utils import timezone

from discovery.Pdf import Pdf
from opinions.models import Opinion
from citations.models import Citation
from justices.models import Justice

import lxml.html
from requests import get
from datetime import datetime
from time import sleep


class Discovery:
    def __init__(self):
        self.opinions = []
        self.category_urls = []
        self.pdfs_to_scrape = []
        self.BASE = 'http://www.supremecourt.gov'
        self.OPINIONS_BASE = self.BASE + '/opinions/'
        self.OPINIONS_MAIN_PAGE = self.OPINIONS_BASE + 'opinions.aspx'
        self.YYYYMMDD = timezone.now().strftime('%Y%m%d')

    def run(self):
        print '[INITATING DISCOVERY - %s]' % timezone.now()
        self.fetch_opinion_category_urls()
        self.get_opinions_from_categories()
        print '[INITIATING OPINION INGEST]'
        self.ingest_new_opinions()
        print '[INITIATION CITATION SCRAPING AND INGEST]'
        self.ingest_new_citations()
        print '[DISCOVERY COMPLETE]'

    def get_url(self, url):
        #TODO: remove wait for production? If so, remove time import 
        sleep(2)
        try:
            request = get(url, headers=settings.REQ_HEADER)
            return request
        except Exception:
            print 'ERROR: fetching %s' % url
            return False

    def fetch_opinion_category_urls(self):
        request = self.get_url(self.OPINIONS_MAIN_PAGE)

        if request and request.status_code == 200:
            html = lxml.html.fromstring(request.text)
            search = "//div[@class='panel-body dslist2']/ul/li/a/@href"
            for category in html.xpath(search):
                self.category_urls.append(self.OPINIONS_BASE + category)
            
    def get_opinions_from_categories(self):
        for category_url in self.category_urls:
            category = category_url.split('/')[-2]
            request = self.get_url(category_url)    

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

                        self.opinions.append(Opinion(
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
        for opinion in self.opinions:
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

                # Report Out
                print 'Skipping: %s' % opinion.name

                # Remove previously discovered opinion from processig list
                del self.opinions[self.opinions.index(opinion)]
                continue

            # Report out
            print 'Ingesting: %s  %s' % (opinion.name, opinion.pdf_url)
 
            # Check if opinion with same name exists. Sometimes SCOTUS fixes and republishes 
            # opinion with same opinion name, but usually a different pdf file name
            opinion.previously_discovered_citations = []
            for previously_discovered in Opinion.objects.filter(name=opinion.name):

                # Report out
                print 'Republished: %s' % opinion.name

                previously_discovered.updated = True
                previously_discovered.save()
                opinion.previously_discovered_citations.append(previously_discovered)
 
                #TODO: should the logic below be removed, and just have check before inserting citation that citation doesn't exist for opinion with smae name?
                # Gather previous opinion's scraped and validated citations
                for citation in Citation.objects.filter(opinion=previously_discovered):
                    opinion.previously_discovered_citations.append(citation.scraped)
                    if citation.validated and citation.validated != citation.scraped:
                        opinion.previously_discovered_citations.append(citation.validated)

            # Ingest new opinion to database
            opinion.save()
            
    def ingest_new_citations(self):
        for opinion in self.opinions:
            local_pdf = settings.PDF_DIR + str(opinion.id) + '.pdf'
            opinion.pdf = Pdf(
                opinion.pdf_url,
                local_pdf,
            )

            print 'Downloading: %s  %s' % (opinion.name, opinion.pdf_url)
            opinion.pdf.download()
            print 'Scraping: %s  %s' % (opinion.name, opinion.pdf_url)
            opinion.pdf.scrape_urls()

            for url in opinion.pdf.urls:
                # Skip citation if ingested in previous discovery
                if url in opinion.previously_discovered_citations:

                    # Report Out
                    print '--Skipping previously discovered citation: %s' % url

                    continue
            
                # Report Out
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

        request = self.get_url(url)
        if not request or request.status_code == 404:
            status[u'citation'] = u'u'
        if request and request.status_code in [302, 301]:
            status[u'citation'] = u'r'

        #TODO: Uncomment this on LIB network.  lx7 doesn't like machine requests off network
        #request = self.get_url(Citation.WAYBACKS['lc'] + url)
        #if request and request.status_code == 200:
        #    status[u'archived_lc'] = True

        request = self.get_url(Citation.WAYBACKS['ia'] + url)
        if request and request.status_code == 200:
            status[u'archived_ia'] = True

        return status

