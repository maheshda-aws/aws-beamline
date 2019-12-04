import logging
from etl.s3 import S3
from etl.emr import EMR
from etl.config import Config
from etl.session import Session
from etl.datewildcard import DateWildcard

class SparkSQL():

    def __init__(self, session, job_config_location, spark_sql_location):
        self.session = session
        self.job_config_file = job_config_file
        self.job_config_location = job_config_location
    
    def 