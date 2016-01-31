import utils
from common.models import Event
from extract_date import extract_dates
from datetime import date
import re
import math



def process_page(query_result):
    print "processing page %s " % query_result.href
    html_text = utils.download_page(query_result.href, timeout=2)
    dates = extract_dates(html_text)
    dates = [d for d in dates if d.dateRange.start >= date.today()]

    if not dates:
        return []

    print "found dates", dates

    rex = re.compile(query_result.title, re.I | re.UNICODE | re.MULTILINE)

    candidate_date = dates[0]
    min_dist = 10000000
    i = 0
    while i != -1 and i < len(html_text):
        match = rex.match(html_text, i)
        if match:
            s = match.start()
            for d in dates:
                if math.abs(d.startPos - s) < min_dist:
                    min_dist = math.abs(d.startPos - s)
                    candidate_date = d

            i = match.end() + 1
        else:
            break

    print "candidate", candidate_date
    return [Event(query_result.title, candidate_date.dateRange.start, candidate_date.dateRange.end)]


def get_events(query_result):
    if query_result and query_result.description:
        dates = extract_dates(query_result.description)
        dates = [d for d in dates if d.dateRange.start >= date.today()]
        if dates:
            return [Event(query_result.title, dates[0].dateRange.start, dates[0].dateRange.end)]

    if query_result and query_result.href and query_result.title:
        return process_page(query_result)

# for testing
if __name__ == "__main__":
    import sys
    print "nothing"