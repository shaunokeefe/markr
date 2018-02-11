from unittest.mock import Mock
import boto3
import moto

from serverless.handler import _copy_content_to_s3


class TestCopyContentToS3(object):

    @moto.mock_s3
    def test_copy(self):
        document = Mock()
        document.raw = 'test string'
        document.test_number.side_effect = lambda: '1234'
        conn = boto3.resource('s3', region_name='ap-southeast-2')
        conn.create_bucket(Bucket='markr-documents')

        _copy_content_to_s3(document)

        body = conn.Object('markr-documents', '1234').get()['Body'].read().decode("utf-8")
        assert body == 'test string'
