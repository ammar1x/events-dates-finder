import requests
from bs4 import BeautifulSoup

from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class QueryResult(object):
    def __init__(self, title, href, description):
        self.title = title
        self.href = href
        self.description = description

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


def query(words, start=0):

    payload = {"q": unicode(words)}
    if start >= 10 and start % 10 == 0:
        payload['start'] = start

    r = requests.get("https://www.google.pl/search", params=payload)
    if r.status_code != 200:
        return ""
    return r.text


def extract_query_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    # result block from google
    result_blocks = soup.find_all("div", class_="g")
    query_results = []

    for result_block in result_blocks:
        a = result_block.find("a")
        em = result_block.find("span", "st")

        href = a['href']
        title = strip_tags(" ".join(list(a.strings)))

        if not href or href.startswith("/url"):
            try:
                href = a['data-href']
            except:
                href = a['href']
                if href.startswith("/url"):
                    href = href.strip("/url?q=")
                    i = href.find("&sa")
                    if i != -1:
                        href = href[:i]

        description = ""
        if em:
            description = strip_tags("".join(list(em.strings)))

        query_results.append(QueryResult(unicode(title), unicode(href), unicode(description)))

    return query_results


def dump(text, filename):
    with open(filename, "w") as f:
        f.write(text)


def round_to_the_nearst_10(n):
    nn = n // 10
    if (nn*10) < n:
        nn += 1
    return nn*10

def get_n_results(query_string, n=10):
    #google take orders by 10
    upper = round_to_the_nearst_10(n)
    qresults = []
    for n in xrange(0, upper, 10):
        qr = extract_query_results(query(query_string, n))
        qresults.append(qr)
    return [it for qres in qresults for it in qres]

if __name__ == "__main__":
    l = get_n_results("python", 30)
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    response = ""
    for a in l:
       try:
           response += a.description
       except Exception as ex:
           raise ex
    print len(l)
    dump(response, "results.html")
