

class PageProcessingException(Exception):
    ''' Error thrown when parsing pages
    '''
    def __init__(self, msg, web_page):
        self.msg = msg
        self.web_page = web_page

    def __str__(self):
        return "Error while processing page %s . %s" % (self.web_page, self.msg)

    def __repr__(self):
        return "Error while processing page %s . %s" % (self.web_page, self.msg)


class EngineQueryError(Exception):
    def __init__(self, msg, status_code=None):
        self.msg = msg
        self.status_code = status_code

    def __str__(self):
        return "EngineQueryError (msg = %s, status code = %s)" % (self.msg, self.status_code)

    def __repr__(self):
        return "EngineQueryError (msg = %s, status code = %s)" % (self.msg, self.status_code)
