import os
import logging
import importlib

import boto3  # type: ignore
from botocore.config import Config  # type: ignore


logger = logging.getLogger(__name__)


class Session:
    """
    A session stores AWS configuration state (e.g. Boto3.Session)
    """
    def __init__(
            self,
            aws_session,
            botocore_max_retries=5
    ):
        """
        Most parameters inherit from Boto3
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

        :param boto3_session: Boto3.Session (Overwrite others Boto3 parameters)
        :param botocore_max_retries: Botocore max retries
        """
        self._aws_session = aws_session
        self._aws_access_key_id = aws_session.get_credentials().access_key
        self._aws_secret_access_key = aws_session.get_credentials().secret_key
        self._aws_session_token = aws_session.get_credentials().session_token
        self._region_name = aws_session.get_credentials().session_token
        self._botocore_max_retries = botocore_max_retries


    @property
    def aws_access_key_id(self):
        return self._aws_access_key_id

    @property
    def aws_secret_access_key(self):
        return self._aws_secret_access_key

    @property
    def aws_session_token(self):
        return self._aws_session_token

    @property
    def region_name(self):
        return self._region_name

    @property
    def botocore_max_retries(self):
        return self._botocore_max_retries

    @property
    def aws_session(self):
        return self._aws_session




