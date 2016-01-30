

class Event(object):

    def __init__(self, name, startDate, endDate=None, desc=None):
        self.name = name
        self.startDate = startDate
        self.endDate = endDate
        self.desc = desc