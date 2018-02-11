import collections
import sys

import xmltodict


class MarkrDocument(object):
    def __init__(self, body):
        self.raw = body
        self.document = xmltodict.parse(body)

    def available_marks(self, student):
        # TODO(shauno): more situation specific error handling - or ok because
        # this is just for testing?
        # TODO(shauno): separate student class
        return int(student['summary-marks']['@available'])

    def _unique_students(self):
        students = {}
        result_list = self.document['mcq-test-results']['mcq-test-result']

        if isinstance(result_list, collections.OrderedDict):
            result_list = [result_list]

        def _available(student):
            return int(student['summary-marks']['@available'])

        for result in result_list:
            student_number = result['student-number']
            available_marks = _available(result)

            if student_number in students:
                if _available(students[student_number]) >= available_marks:
                    continue

            students[student_number] = result
        return students


def import_function(filename):
    with open(filename) as f:
        MarkrDocument(f.read())


if __name__ == "__main__":
    import_function(sys.args[0])
