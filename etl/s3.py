
import logging
from urllib.parse import urlparse
from boto3 import client

logger = logging.getLogger(__name__)


class S3:
    """
    S3 representation
    """
    def __init__(self, session):
        self._session = session
        self._client_s3: client = session.aws_session.client(service_name="s3")

    def get_object(self, s3_object_name):
        self.bucket_name = urlparse(s3_object_name).
        self._client_s3.get_object(object_name)
