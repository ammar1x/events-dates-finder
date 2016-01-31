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


def dump(text, filename):
    with open(filename, "w") as f:
        f.write(text)


def read_file(filepath):
    cont = ""
    with open(filepath) as f:
        cont = f.read()
    return cont
