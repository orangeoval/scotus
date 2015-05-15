# -*- coding: utf-8 -*-

from scotus import settings
from citations.models import Citation

from urlparse import urlparse
from time import sleep
import requests

class Url:
    TIMEOUT = 30
    HEADERS = settings.REQ_HEADER
    SLEEP = 2

    @classmethod
    def get(cls, url=False, err=True):
        if url:
            # Wait 2 seconds between requests
            sleep(cls.SLEEP)
            check = urlparse(url)

            if not check.scheme:
                url = 'http://' + url 

            try:
                return requests.get(url,
                                    headers=cls.HEADERS,
                                    timeout=cls.TIMEOUT,)
            except Exception:
                pass
       
        if err:
            print 'ERROR: fetching %s' % url

        return False

    @classmethod
    def check_status(cls, url=False):
        status = {
            'status': 'a',
            'archived_lc': False,
            'archived_ia': False,
        }
 
        request = Url.get(url)

        if not request or request.status_code == 404:
            status['status'] = 'u'
        # 300 status codes aren't captured, so must compare before and after urls
        elif request and (request.url != url):
            if request.url != url + '/':
                if request.url.split('://')[1] != url.split('://')[1]:
                    status['status'] = 'r'

        request = Url.get(Citation.WAYBACK_IA + url)
        if request and request.status_code == 200:
            status['archived_ia'] = True

        #TODO: add check for LC

        return status
