import sys

import xmltodict


class MarkrDocument(object):
    def __init__(self, body):
        self.raw = body
        self.document = xmltodict.parse(body)


def import_function(filename):
    with open(filename) as f:
        MarkrDocument(f.read())


if __name__ == "__main__":
    import_function(sys.args[0])
