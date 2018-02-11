import pytest

from serverless import handler


class TestMarkrDocument(object):
    def test_initialisation(self):
        contents = open('test/data/sample_results.xml').read()
        try:
            document = handler.MarkrDocument(contents)
        except:
            pytest.fail("Failed to initialise MarkrDocument")

        assert document.raw == contents
        assert 'mcq-test-results' in document.document
        results_list = document.document['mcq-test-results']['mcq-test-result']
        assert len(results_list) == 100

    def test_gets_available_marks(self):
        contents = open('test/data/single_result.xml').read()
        student = {'summary-marks': {'@available': 20}}

        document = handler.MarkrDocument(contents)

        assert document.available_marks(student) == 20

    def test_gets_unique_students_duplicates(self):
        student_number = '002299'
        contents = open('test/data/duplicate_user_1.xml').read()

        document = handler.MarkrDocument(contents)
        students = document._unique_students()

        assert len(students) == 1
        student = students[student_number]
        assert document.available_marks(student) == 21

        contents = open('test/data/duplicate_user_2.xml').read()

        document = handler.MarkrDocument(contents)
        students = document._unique_students()

        assert len(students) == 1
        student = students[student_number]
        assert document.available_marks(student) == 21

    def test_validation(self):
        # TODO(shauno)
        pass

    def test_mean_for_single_student(self):
        contents = open('test/data/single_result.xml').read()
        document = handler.MarkrDocument(contents)

        assert document.mean() == 13.0

    def test_mean_for_multiple_students(self):
        contents = open('test/data/three_results.xml').read()
        document = handler.MarkrDocument(contents)

        assert document.mean() == 11.67

    def test_count_for_single_student(self):
        contents = open('test/data/single_result.xml').read()
        document = handler.MarkrDocument(contents)

        assert document.count() == 1

    def test_count_for_duplicate_students(self):
        contents = open('test/data/duplicate_user_1.xml').read()
        document = handler.MarkrDocument(contents)

        assert document.count() == 1
