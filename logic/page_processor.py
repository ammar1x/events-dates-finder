import requests
from bs4 import BeautifulSoup
import re
from utils import strip_tags
import utils
from extract_date import extract_dates

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


def process_page(query_result):
    print "processing page %s " % query_result
    html_text = utils.download_page(query_result.href)
    dates = extract_dates(html_text)
    print len(dates)
    print dates
    if dates:
        return [Event(query_result.title, dates[0].dateRange.start, dates[0].dateRange.end)]


def get_events(query_result):
    if query_result and query_result.description:
            dates = extract_dates(query_result.description)
            if dates:
                return [Event(query_result.title, dates[0].dateRange.start, dates[0].dateRange.end)]

    if query_result and query_result.href and query_result.title:
        return process_page(query_result)





if __name__ == "__main__":
    import sys
    #
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    #
    # title = "festiwal gdynia"
    # ress = from_file("results.html")
    # for res in ress:
    #
    #     if res.title and res.href:
    #         try:
    #             print "searching " + res.href + " for " + res.title
    #             text = download_page(res.href)
    #             print extract_text(text, res.title)
    #         except IOError as er:
    #             print er
    #         except Exception as ex:
    #             print ex
