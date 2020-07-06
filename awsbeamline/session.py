import os
import uuid
import boto3
import logging
import importlib
import urllib3
from datetime import datetime
from botocore.config import Config
from urllib.parse import urlparse

import awsbeamline.constants as constants
from awsbeamline.s3 import S3
from awsbeamline.emr import EMR 
from awsbeamline.emr_config import EMRConfig
from awsbeamline.task_manager import TaskManager
from awsbeamline.workload_config import WorkloadConfigParser
from awsbeamline.compute_manager import ComputeManager
from awsbeamline.datewildcard import ReplaceWildcard



logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%dT%H:%M:%S')


class Session:
    """
    Session module maintains the session state for a workload profile. This is the entrypoint into Beamline.
    """

    def __init__(self,
                 job_config_location: str,
                 run_date_str: str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                 instance_id: int = None,
                 profile_name: str = None,
                 run_date_format: str = "%Y-%m-%dT%H:%M:%S"):
        """
        Arguments:
            job_config_location {str} -- Location of the job profile config file
            profile_name {str} -- Profile name for the beamline session
            run_date {str} -- Input date for the job.

        Keyword Arguments:
            run_date_format {str} -- Input date format (default: {"%Y-%m-%dT%H:%M:%S"})
        """
        logging.info("Initializing beamline session.")
        if instance_id is None:
            self.session_instance_id = uuid.uuid4().int
        else:
            self.session_instance_id = instance_id

        self.job_config_location = job_config_location
        self.session_date_str = run_date_str
        self.session_date_format = run_date_format
        if profile_name:
            self.profile_name = profile_name
        else:
            logging.info("Profile name is not provided. Beamline would generate a profile_name")
            self.profile_name = self.session_instance_id
        logging.info("Profile Name: {}".format(self.profile_name))
        self.aws_session = boto3.Session()
        #self.s3_session = self.aws_session.client(service_name="s3")
        self.batch_session = self.aws_session.client(service_name="batch")
        #self.job_config = WorkloadConfig(job_config_location)
        self.constants = constants

    @property
    def emr_session(self):
        return EMR(session=self)

    @property
    def s3_session(self):
        return S3(session=self)

    @property
    def compute_manager(self):
        return ComputeManager(session=self)

    @property
    def task_manager(self):
        return TaskManager(session=self)

    @property
    def emr_config(self):
        return EMRConfig(session=self, emr_config_file="config/emr.yaml")

    @property
    def session_date(self):
        return datetime.strptime(self.session_date_str, self.session_date_format)
    
    @property
    def date_wildcards(self):
        return ReplaceWildcard(date=self.session_date)

    @property
    def job_instance_config(self):
        if urlparse(self.job_config_location).scheme == "s3":
            job_instance_config = self.s3_session.read_s3_file_content(self.job_config_location)
            #job_config = WorkloadConfig(job_config_file_location=self.s3_session.read_s3_file_content(self.job_config_location))
        else:
            job_instance_config = open(self.job_config_location)

        return job_instance_config
    
    @property
    def config_parser(self):
        return WorkloadConfigParser(self.job_instance_config)


#s = Session(job_config_location="config/examples/job_definition/spark_sql.yaml", profile_name="test", run_date_str="2019-09-19T15:38:10")
#print(s.session_date.strftime("%Y"))


