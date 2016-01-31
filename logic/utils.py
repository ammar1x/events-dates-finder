from HTMLParser import HTMLParser
from common.utils import dump, read_file
import requests


class MLStripper(HTMLParser):
    '''Helper class for striping html text from tags. This class
    was downloaded from https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python'''

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    '''
    :param html: html text string
    :return: text without tags
    '''
    s = MLStripper()
    s.feed(html)
    return s.get_data()


headers = {
    'user-agent': 'Mozilla/5.0 (Windows) Gecko/20100101 Firefox/44.0',
    'accept': "image/webp,image/*,*/*;q=0.8",
    'accept-language': 'accept-language:en-US,en;q=0.8,pl;q=0.6,ar;q=0.4'
}


def download_page(url, timeout=None):
    '''
    :param url: the url of the page to download
    :param timeout: maximum time to wait until the web site response to the query
    :return: requested page in html
    '''
    if timeout:
        r = requests.get(url, headers=headers, timeout=timeout)
    else:
        r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return ""
    return r.text


def dump_query_results(query_results, filepath):
    res = "\n".join(["%s :<>: %s :<>: %s" % (qr.title, qr.href, qr.description) for qr in query_results])
    dump(res, filepath)
