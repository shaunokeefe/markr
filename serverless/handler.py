import collections
import json
import logging

import numpy as np
import boto3
import xmltodict


class MarkrValidationError(object):
    pass


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

    def validate(self):
        # TODO(shauno): come back to this
        pass

    def test_number(self):
        # TODO(shauno): make this better
        return self.document['mcq-test-results']['mcq-test-result']['test-id']

    def _scores(self):
        return [float(s['summary-marks']['@obtained']) for s in self._unique_students().values()]

    def mean(self):
        # mean - the mean of the awarded marks
        return round(float(sum(self._scores())) / max(self.count(), 1), 2)

    def count(self):
        # count - the number of students who took the test
        return len(self._unique_students())

    def percentiles(self):
        # p25, p50, p75 - the 25th percentile, median,
        # and 75th percentile scores
        # TODO(shauno): scores function or something
        scores = [float(s['summary-marks']['@obtained']) for s in self._unique_students().values()]
        return {
            'p25': np.percentile(scores, 25),
            'p50': np.percentile(scores, 50),
            'p75': np.percentile(scores, 75)
        }


def _copy_content_to_s3(document):
    s3 = boto3.resource('s3')
    # TODO(shauno): bucket in an env variable setting
    obj = s3.Object('markr-documents-shauno', document.test_number())
    obj.put(Body=document.raw.encode())


def import_function(event, context):
    # validate request
    # - check for text/xml+markr header and 4--
    # - check document has necessary fields

    content = event['body']
    document = MarkrDocument(content)
    response = {
        "statusCode": 200
    }

    try:
        document.validate()
    except MarkrValidationError:
        logging.error("Validation error")

    _copy_content_to_s3(document)
    return response


def _copy_content_from_s3(test_number):
    s3 = boto3.resource('s3')
    # TODO(shauno): stream instead of read
    obj = s3.Object('markr-documents-shauno', test_number)
    content = obj.get()['Body'].read().decode('utf-8')
    return MarkrDocument(content)


def results_function(event, context):
    # TODO(shauno): tests
    test_number = event["pathParameters"]["test_id"]
    # TODO(shauno): handle missing document
    d = _copy_content_from_s3(test_number)

    body = {'mean': d.mean(), 'count': d.count()}
    body.update(d.percentiles())
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
