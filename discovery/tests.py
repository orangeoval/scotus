from django.test import TestCase
from scotus import settings
from discovery.Pdf import Pdf
from discovery.Pdf import Url

class PdfTestCase(TestCase):
    def test_urls_as_expected(self):
        """Expected urls are scraped"""
        checks = {settings.BASE_DIR + '/discovery/pdfs/United_States_v._Alvarez.pdf': [
            'http://www.cmohs.org/recipient-archive.php',
            'http://articles.philly.com/2004-02-11/news/25374213_1_medals-military-imposters-distinguished-flying-cross',
            'http://www.chicagotribune.com/news/local/chi-valor-oct25,0,4301227.story?page=1',
            'http://articles.chicagotribune.com/1994-10-21/news/9410210318_1_congressional-medal-highest-fritz',
            'http://www.nytimes.com/2002/04/29/business/at-fox-news-the-colonel-who-wasn-t.html?pagewanted=all&src=pm',
            'http://www.nydailynews.com/news/crime/war-crime-fbi-targets-fake-heroes-article-1.249168',
            'http://www.justice.gov/usao/waw/press/2007/sep/operationstolenvalor.html',
            'http://triblive.com/usworld/nation/1034434-85/court-military-law-false-medals-supreme-valor-act-federal-free',
            'http://www.history.army.mil/html/moh/mohstats.html',
        ]}

        for document, citations in checks.iteritems():
            pdf = Pdf()
            pdf.local_file = document
            pdf.extract_text()
            pdf.extract_urls_from_text()
            self.assertEqual(pdf.urls, citations)


class UrlTestCase(TestCase):
    def test_request(self):
        """Expected request returns"""
        checks = {'http://www.google.com': 200,
                  'www.google.com': 200,
                  'http://kjhkjhkjhkjhkjhkjhkjhkjhkjhkjh.com': False,
        }

        for url, response in checks.iteritems():
            if response:
                request = Url.get(url)
                self.assertEqual(request.status_code, response)
            else:
                self.assertEqual(Url.get(url, False), response)
