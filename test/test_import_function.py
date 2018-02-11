from unittest.mock import Mock, patch

from serverless import handler


class TestImportFunction(object):
    @patch('serverless.handler.MarkrDocument')
    def test_passes_event_body(self, markr_document_constructor):
        body_contents = 'test_body'
        event = {'body': body_contents}
        context = {}
        markr_document_constructor.return_value = document = Mock()
        document.validate.return_value = True

        handler.import_function(event, context)

        markr_document_constructor.assert_called_with(body_contents)

    @patch('serverless.handler.MarkrDocument')
    def test_200_on_success(self, markr_document_constructor):
        body_contents = 'test_body'
        event = {'body': body_contents}
        context = {}
        markr_document_constructor.return_value = document = Mock()
        document.validate.return_value = True

        response = handler.import_function(event, context)

        assert response['statusCode'] == 200

