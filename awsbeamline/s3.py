
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
        file_path = "/tmp/" + str(self._session.session_instance_id)
        logging.info("Downloading file to {}".format(file_path))
        bucket_name = urlparse(s3_object).hostname
        object_key = urlparse(s3_object).path[1:]
        self._client_s3.download_file(Bucket=bucket_name, Key=object_key, Filename=file_path)
        return file_path
    
    def read_s3_file_content(self, s3_object):
        bucket_name = urlparse(s3_object).hostname
        object_key = urlparse(s3_object).path[1:]
        object_body = self._client_s3.get_object(Bucket=bucket_name,
                                   Key=object_key)['Body'].read().decode("utf-8")
        logging.debug(object_body)
        return self._session.date_wildcards.replace_wildcard(wildcard_string = object_body)


    def upload_object(self, bucket, object_path, file):
        logging.info("Uploading file:{}. Destination Bucket:{}, Path:{} ".format(file, bucket, object_path ))
        return self._client_s3.upload_file(Filename=file, Bucket=bucket, Key=object_path)
    
    def put_s3_object_content(self, s3_object: str, content:str):
        logging.info("Writing content to S3. Object: {}".format(s3_object))
        bucket_name = urlparse(s3_object).hostname
        object_key = urlparse(s3_object).path[1:]
        self._client_s3.put_object(Bucket = bucket_name, Key = object_key, Body = content)





