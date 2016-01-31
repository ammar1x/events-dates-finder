from HTMLParser import HTMLParser
from common.utils import dump, read_file
import requests

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)



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


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def dump_query_results(query_results, filepath):
    res = "\n".join(["%s :<>: %s :<>: %s" % (qr.title, qr.href, qr.description) for qr in query_results])
    dump(res, filepath)

# def read_query_results(filepath):
#     cont = read_file(filepath)
#     lines = cont.split("\n")
#     qrs = []
#     for line in lines:
#         ts = [t.strip() if t else "" for t in line.split(":<>:")]
#         qrs.append(search.QueryResult(ts[0], ts[1], ts[2]))
#     return qrs

