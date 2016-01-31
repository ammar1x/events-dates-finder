import requests
from bs4 import BeautifulSoup
import re
from utils import strip_tags
from search import QueryResult
from datetime import date
from random import randint


class PageProcessingException(Exception):

    def __init__(self, msg, web_page):
        self.msg = msg
        self.web_page = web_page

    def __str__(self):
        return "Error while processing page %s . %s" % (self.web_page, self.msg)

    def __repr__(self):
        return "Error while processing page %s . %s" % (self.web_page, self.msg)


class Event(object):
    def __init__(self, title, startDate, endDate=None, desc=None):
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
        self.desc = desc

    def __str__(self):
        return "%s (%s)" % (self.title, self.startDate)

    def __repr__(self):
        return "%s (%s)" % (self.title, self.startDate)


def get_events(query_result):
    y = 2016
    m = randint(1, 3)
    d = randint(1, 28)

    return [Event(query_result.title, date(y, m, d))]



ress = [r"[0-9]{2].[0-9]{2].[0-9]{4]"]

for res in ress:
    prog = re.compile(res)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows) Gecko/20100101 Firefox/44.0',
    'accept': "image/webp,image/*,*/*;q=0.8",
    'accept-language': 'accept-language:en-US,en;q=0.8,pl;q=0.6,ar;q=0.4'
}


def download_page(url):
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return ""
    return r.text


def extract_events(html, title):
    b = BeautifulSoup(html, 'html.parser')
    body = b.find('body')
    a = re.compile(title, re.I)
    text = strip_tags("".join(list(body.strings)))
    print text
    ms = re.findall(title, text, re.I)
    print ms
    for m in ms:
        print title
        print m.group(0)


def extract_text(html, title):
    b = BeautifulSoup(html, 'html.parser')
    return b.get_text()



if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')

    title = "festiwal gdynia"
    ress = from_file("results.html")
    for res in ress:

        if res.title and res.href:
            try:
                print "searching " + res.href + " for " + res.title
                text = download_page(res.href)
                print extract_text(text, res.title)
            except IOError as er:
                print er
            except Exception as ex:
                print ex
