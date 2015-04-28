from django.test import TestCase
from discovery.Pdf import Pdf

class PdfTestCase(TestCase):
    def setUp(self):
        pdf = Pdf()
        pdf.local_file = 'docs/pdfs/10664.pdf'
        pdf.extract_text()
        pdf.extract_urls_from_text()

    def test_urls_as_expected(self):
        """Expected urls are scraped"""
        citations = [
            'http://www.cmohs.org/recipient-archive.php',
            'http://articles.philly.com/2004-02-11/news/25374213_1_medals-military-imposters-distinguished-flying-cross',
            'http://www.chicagotribune.com/news/local/chi-valor-oct25,0,4301227.story?page=1',
            'http://articles.chicagotribune.com/1994-10-21/news/9410210318_1_congressional-medal-highest-fritz',
            'http://www.nytimes.com/2002/04/29/business/at-fox-news-the-colonel-who-wasn-t.html?pagewanted=all&src=pm',
            'http://www.nydailynews.com/news/crime/war-crime-fbi-targets-fake-heroes-article-1.249168',
            'http://www.justice.gov/usao/waw/press/2007/sep/operationstolenvalor.html',
            'http://triblive.com/usworld/nation/1034434-85/court-military-law-false-medals-supreme-valor-act-federal-free',
            'http://www.history.army.mil/html/moh/mohstats.html',
        ]
        self.assertEqual(pdf.urls, citations)
