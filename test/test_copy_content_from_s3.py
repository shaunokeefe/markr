from unittest.mock import patch, Mock
import boto3
import moto

from serverless.handler import _copy_content_from_s3


class TestCopyContentToS3(object):

    #def test_passes_event_body(self, markr_document_constructor, copy_s3_mock):
    #    body_contents = 'test_body'
    #    event = {'body': body_contents}
    #    context = {}
    #    markr_document_constructor.return_value = document = Mock()
    #    document.validate.return_value = True

    @moto.mock_s3
    @patch('serverless.handler.MarkrDocument')
    def test_copy(self, markr_document_constructor):
        markr_document_constructor.return_value = Mock()

        conn = boto3.resource('s3', region_name='ap-southeast-2')
        conn.create_bucket(Bucket='markr-documents-shauno')
        conn.Object('markr-documents-shauno', '1234').put(Body='test string')

        _copy_content_from_s3('1234')

        markr_document_constructor.assert_called_with('test string')
