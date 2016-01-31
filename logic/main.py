import search
import page_processor


def cons_equal(wordsi, wordsj):
    es = 0
    for i in xrange(min(len(wordsi), len(wordsj))):
        if wordsi[i] == wordsj[i]:
            es += 1
    return es


def deduplicate(events):
    '''
    Remove events that are simliar. Two events are similar if they contain 3 exact words.
    :param events: list of events
    :return: list of events without duplicates
    '''
    dups = []
    for i in xrange(len(events)):
        wordsi = events[i].title.lower().split()
        for m in xrange(len(wordsi)):
            for j in xrange(i + 1, len(events)):
                wordsj = events[j].title.lower().split()
                for k in xrange(len(wordsj)):
                    if cons_equal(wordsi[m:], wordsj[k:]) == 3:
                        dups.append(events[j])
                        break

    print "found duplicates", dups
    for dup in dups:
        if dup in events:
            events.remove(dup)
    return events


def get_n_events(query_string, n=10, query_engine=search.query_google):
    query_results = search.get_n_results(query_string, n, query_engine=query_engine)
    events = []
    for query_result in query_results:
        query_events = []
        if not query_result.href or not query_result.href.startswith("http"):
            print "query result contains invalid string %s" % str(query_result.href)
            continue
        try:
            query_events = page_processor.get_events(query_result)
        except Exception as ex:
            print "error while getting events for query result %s" % query_result
            print ex
        if query_events:
            events.extend(query_events)
    print events
    filtered = deduplicate(events)
    events.sort(key=lambda h: h.startDate)

    print filtered
    if not filtered and query_engine == search.query_google:
        return get_n_events(query_string, n, search.query_bing)

    return filtered
