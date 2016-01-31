

class Event(object):
    '''
    Data type for representing Event. Acts like a transfer object between logic and gui.
    '''
    def __init__(self, title, startDate, endDate=None, desc=None, src=None):
        '''
        :param title: the title of the event
        :param startDate: start date of the event
        :param endDate: end date of the event. Not required.
        :param desc: description of the event. Not required.
        :param src: web url of the event. Not require.
        :return:
        '''
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
        self.desc = desc
        self.src = src

    def __str__(self):
        return "%s (%s)" % (self.title, self.startDate)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not other:   return False
        if type(other) != type(self): return False
        return self.title == other.title and self.startDate == other.startDate and self.endDate == other.endDate

    def __repr__(self):
        return "%s (%s)" % (self.title, self.startDate)


class DateRange(object):
    '''
    Represents date range.
    '''
    def __init__(self, start, end):
        '''
        :param start: the start date of the range.
        :param end: the end date of the range.
        :return: new Date Range
        '''
        self.start = start
        self.end = end

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not other:
            return False
        if type(other) != type(self):
            return False
        return self.start == self.start and self.end == self.end

    def __repr__(self):
        s = self.start
        e = self.end
        if not e:
            e = ""
        else:
            e = "-" + str(e)

        return "%s%s" % (s, e)

    def __str__(self):
        s = self.start
        e = self.end
        if not e:
            e = ""
        else:
            e = " - " + str(e)

        return "%s%s" % (s, e)
