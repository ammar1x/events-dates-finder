# -*- coding: utf-8 -*-
import re
from datetime import date
import pprint

rxDelimiter = r"[ -/.]"
rxDay = r"[0-9]{2}"
rxMonth = r"[0-1][0-9]"
rxYear = r"[0-9]{4}"
rxPolishMonth = r"(stycz|lut|mar|kwie|maj|czerw|lip|sierp|wrze|pa|listopad|grud)[^\s]+"

# dd/mm/yyyy
european_date_format = "[^-]" + "(" + rxDay + rxDelimiter + rxMonth + rxDelimiter + rxYear + ")"
# mm/dd/yyyy
american_date_format = "(" + rxMonth + rxDelimiter + rxDay + rxDelimiter + rxYear + ")"
# yyyy/mm/dd
technical_date_format = "(" + rxYear + rxDelimiter + rxMonth + rxDelimiter + rxDay + ")"
# dd polishMonth yy
polish_date_format = "[^-]" + "(" + rxDay + rxDelimiter + rxPolishMonth + rxDelimiter + rxYear + ")"
# dd polishMonth
polish1_date_format = "[^-]" + "(" + rxDay + rxDelimiter + rxPolishMonth + rxDelimiter + "^(" + rxYear + ")" + ")"

# ranges
european_date_format_range = "(" + rxDay + "[-]" + rxDay + rxDelimiter + rxMonth + rxDelimiter + rxYear + ")"
polish_date_format_range = "(" + rxDay + "[-]" + rxDay + rxDelimiter + rxPolishMonth + rxDelimiter + rxYear + ")"
polish1_date_format_range = "(" + rxDay + "[-]" + rxDay + rxDelimiter + rxPolishMonth + rxDelimiter + "^(" + rxYear + ")" + ")"

formats = [
    european_date_format, technical_date_format,
    polish_date_format, polish1_date_format,
    # ranges
    european_date_format_range,
    polish_date_format_range,
    polish1_date_format]

polish_months_prefix = [u"-", u"stycz", u"lut", u"marz", u"kwiec", u"maj", u"czerw", u"lip", u"sierp", u"wrze", u"pa",
                        u"list", u"grud"]


def to_py_date(tokens, seqs):
    y, m, d = 0, 0, 0
    for (token, f) in zip(tokens, seqs):
        if f == 'y':
            if len(token) == 2:
                y = int("20"+token)
            else:
                y = int(token)
        elif f == 'm':
            m = int(token)
        elif f == 'd':
            d = int(token)
    return date(y, m, d)


def polish_py_date(tokens, format1=""):
    y, m, d = 0, 0, 0
    polish_month = tokens[1]
    if len(tokens[2]) == 2:
        y = int("20"+tokens[2])
    else:
        y = int(tokens[2])

    for (i, polish_month_prefix) in enumerate(polish_months_prefix):
        if polish_month.startswith(polish_month_prefix):
            m = i
            break
    d = int(tokens[0])
    return date(y, m, d)



def polish1_py_date(tokens, format1=""):
    return polish_py_date(tokens + [str(date.today().year)])


def split(s):
    return re.split(rxDelimiter, s)


def split_range(string):
    first, second = "", ""
    for (i, chr) in enumerate(string):
        if chr == "-":
            first = string[:i] + string[i + 3:]
            second = string[i + 1:]
            break
    return first, second


def handle_date_range(s, format1, date_handler=to_py_date):
    first, second = split_range(s)
    return DateRange(date_handler(split(first), format1), date_handler(split(second), format1))


class DateRange(object):

    def __init__(self, start, end):
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


class DateInfo:

    def __init__(self, strdate, format):
        self.strstart = strdate
        self.format = format
        self.dateRange = natural_to_date_mappers[self.format](strdate)

    def __str__(self):
        return self.dateRange.__str__()

    def __repr__(self):
        return self.dateRange.__repr__()



natural_to_date_mappers = {
    european_date_format: lambda s: DateRange(to_py_date(split(s), 'dmy'), None),
    technical_date_format: lambda s: DateRange(to_py_date(split(s), 'ymd'), None),
    polish_date_format: lambda s: DateRange(polish_py_date(split(s)), None),
    polish1_date_format: lambda s: DateRange(polish1_py_date(split(s)), None),
    european_date_format_range: lambda s: handle_date_range(s, 'dmy'),
    polish_date_format_range: lambda s: handle_date_range(s, 'dmy', polish_py_date),
    polish1_date_format_range: lambda s: handle_date_range(s, 'dmy', polish1_py_date),
}

rexs = []
for format in formats:
    rexs.append(re.compile(format, re.IGNORECASE | re.UNICODE | re.MULTILINE))



def extract_dates(string):
    dates = []
    for (rex, format) in zip(rexs, formats):

        start_pos = 0
        n = len(string)
        # print format
        while 0 <= start_pos < n:
            match = rex.search(string, start_pos)
            if match:
                # print "\t" + match.group()
                try:
                    dates.append(DateInfo(match.group(1), format))
                except Exception as ex:
                    print "error while processing date %s" % match.group(1)
                    print ex
                start_pos = match.end() + 1
            else:
                break
    return dates


from utils import download_page

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    page_text = download_page(
        "http://starforce.eu/")
    date_strs = extract_dates(page_text)
    for date_str in date_strs:
        print date_str
