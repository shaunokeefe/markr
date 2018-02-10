import pytest

import document_import


class TestMarkrDocument(object):
    def test_initialisation(self):
        contents = open('test/data/sample_results.xml').read()
        try:
            document = document_import.MarkrDocument(contents)
        except:
            pytest.fail("Failed to initialise MarkrDocument")

        assert document.raw == contents
        assert 'mcq-test-results' in document.document
        results_list = document.document['mcq-test-results']['mcq-test-result']
        assert len(results_list) == 100
