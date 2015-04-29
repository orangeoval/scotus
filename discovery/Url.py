# -*- coding: utf-8 -*-

from scotus import settings
from urlparse import urlparse
from time import sleep
import requests

class Url:
    TIMEOUT = 30
    HEADERS = settings.REQ_HEADER
    SLEEP = 2

    @classmethod
    def get(cls, url):
        #TODO: remove wait for production? If so, remove time import 
        sleep(cls.SLEEP)

        check = urlparse(url)
        if not check.scheme:
            url = 'http://' + url 

        try:
            return requests.get(url,
                                headers=cls.HEADERS,
                                timeout=cls.TIMEOUT,)
        except Exception:
            print 'ERROR: fetching %s' % url
            return False
