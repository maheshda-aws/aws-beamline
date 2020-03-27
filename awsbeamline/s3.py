
import logging
from urllib.parse import urlparse
from boto3 import client

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class S3:
    """[summary]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, session):
        self._session = session
        self._client_s3: client = self._session.aws_session.client(service_name="s3")

    def get_s3_file(self, s3_object):
        file_path="/tmp/"+self._session.session_instance_id
        bucket_name = urlparse(s3_object).hostname
        object_key = urlparse(s3_object).path[1:]
        self._client_s3.download_file(Bucket=bucket_name, Key=object_key, Filename=file_path).get('Body').read()
        return file_path

    def upload_object(self, bucket, object_path, file):
        logging.info("Uploading file:{}. Destination Bucket:{}, Path:{} ".format(file, bucket, object_path ))
        return self._client_s3.upload_file(Filename=file, Bucket=bucket, Key=object_path)

    def exists(self, bucket, object_path):
        print(self._client_s3.list_objects(Bucket=bucket, Prefix=object_path))
        if self._client_s3.list_objects(Bucket=bucket, Prefix=object_path).get("Contents") is None:
            return False
        else:
            return True


