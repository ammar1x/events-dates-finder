import search
import page_processor
import utils


def get_n_events(query_string, n=10):
    query_results = search.get_n_results(query_string, n, query_engine=search.query_google)
    #utils.dump_query_results(query_results, "results1.html")
    all_events = []
    for query_result in query_results:
        events = page_processor.get_events(query_result)
        if events:
            all_events.extend(events)
    all_events.sort(key=lambda h: h.startDate)
    return all_events

