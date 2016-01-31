import requests
from bs4 import BeautifulSoup
import time
from utils import strip_tags


class EngineQueryError(Exception):
    def __init__(self, msg, status_code=None):
        self.msg = msg
        self.status_code = status_code

    def __str__(self):
        return "EngineQueryError (msg = %s, status code = %s)" % (self.msg, self.status_code)

    def __repr__(self):
        return "EngineQueryError (msg = %s, status code = %s)" % (self.msg, self.status_code)


class QueryResult(object):
    def __init__(self, title, href, description):
        self.title = unicode(title)
        self.href = unicode(href)
        self.description = unicode(description)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


def query_bing(words, start=0):
    print start
    return query("http://www.bing.com/search", words, {'first': start}, start)


def query_google(words, start=0):
    return query("http://www.google.pl/search", words, {'start': start}, start)


def query(web_page, words, params, start=0):
    payload = {"q": unicode(words)}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows) Gecko/20100101 Firefox/44.0',
        'accept': "image/webp,image/*,*/*;q=0.8",
        'accept-language': 'accept-language:en-US,en;q=0.8,pl;q=0.6,ar;q=0.4'

    }

    if start >= 10 and start % 10 == 0:
        payload.update(params)
    r = requests.get(web_page, params=payload, headers=headers)

    if r.status_code != 200:
        print r.request.headers
        print r.text
        raise EngineQueryError("Cannot download search results from %s" % web_page, r.status_code)
    return r.text


def extract_info(f):
    info = ""
    try:
        info = f()
    except:
        pass
    return info


def extract_bing_query_results(html):
    soup = BeautifulSoup(html, 'html.parser')

    results_blocks = soup.find_all("li", class_="b_algo")
    query_results = []
    for result_block in results_blocks:
        a = result_block.find("a")
        em = result_block.find("p")
        href = extract_info(lambda: a['href'])
        title = extract_info(lambda: "".join(list(a.strings)))
        description = extract_info(lambda: "".join(list(em.strings)))
        if href:
            query_results.append(QueryResult(title, href, description))
    return query_results


def extract_google_query_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    # result block from google
    result_blocks = soup.find_all("div", class_="g")
    query_results = []

    for result_block in result_blocks:
        a = result_block.find("a")
        em = result_block.find("span", "st")

        href = extract_info(lambda: a['href'])
        title = extract_info(lambda: "".join(list(a.strings)))

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

        description = extract_info(lambda: strip_tags("".join(list(em.strings))))

        query_results.append(QueryResult(unicode(title), unicode(href), unicode(description)))

    return query_results


def round_to_the_nearst_10(n):
    nn = n // 10
    if (nn * 10) < n:
        nn += 1
    return nn * 10


def get_n_results(query_string, n=10, query_engine=query_bing):
    upper = round_to_the_nearst_10(n)
    qresults = []
    for n in xrange(0, upper, 10):
        result_extractor = None

        if query_engine == query_google:
            result_extractor = extract_google_query_results
        else:
            result_extractor = extract_bing_query_results

        qr = result_extractor(query_engine(query_string, n))
        time.sleep(0.5)
        qresults.append(qr)
    return [it for qres in qresults for it in qres]


if __name__ == "__main__":
    l = get_n_results("festiwal gdynia", 10, query_google)
    print "L = "

    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')
    response = ""
    for a in l:
        try:
            response += a.href + " :<>: " + a.title + "\n"
        except Exception as ex:
            pass
    print len(l)
    dump(response, "results.html")
