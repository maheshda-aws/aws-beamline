import os
import time
import logging
from awsbeamline.datewildcard import ReplaceWildcard


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class TaskManager():
    def __init__(self, session):
        self.session = session
        self.task_instance_file = "s3://" + self.session.constants.BEAMLINE_BUCKET_NAME + "/task_instaces/" + self.session.profile_name + "/" + str(self.session.session_instance_id) + ".yaml"
        self.task_instance_executable = "s3://" + self.session.constants.BEAMLINE_BUCKET_NAME + "/task_instaces/" + self.session.profile_name + "/" + str(self.session.session_instance_id)

    def create_task_instance(self):
        logging.info("Creating instance config.")
        self.session.s3_session.put_s3_object_content(s3_object=self.task_instance_file, content=self.session.job_instance_config)
        self.session.s3_session.put_s3_object_content(s3_object=self.task_instance_executable, content=self.session.s3_session.read_s3_file_content(self.session.config_parser.executable_location))
        return True


    def register_task(self, overwrite):
        logging.info("Registering task definition")
        object_path = "config/" + self.session.job_config.job_type + "/" + self.session.job_config.namespace + "/" + self.session.job_config.job_name
        if overwrite:
            self.session.s3_session.upload_object(
                                                  bucket=self.session.constants.BEAMLINE_BUCKET_NAME,
                                                  object_path=object_path,
                                                  file=self.session.job_config_location
                                                  )
        elif self.session.s3_session.exists(bucket=self.session.constants.BEAMLINE_BUCKET_NAME, object_path=object_path):
            logging.error("The task definition already exists")
            raise Exception("Task definition with the same name already exists. Try -o or --overwrite option if you want to overwrite.")
        else:
            self.session.s3_session.upload_object(
                                                  bucket=self.session.constants.BEAMLINE_BUCKET_NAME,
                                                  object_path=object_path,
                                                  file=self.session.job_config_location
                                                 )
        logging.info("Task definition successfully registered/overwritten.")

    def execute_sparksql_task(self):
        try:
            self.create_task_instance()
            cluster_id =self.session.compute_manager.start_compute().get("JobFlowId")
            logging.info("Cluster Id: {}".format(cluster_id))
            cluster_state = self.session.compute_manager.get_cluster_status(cluster_id)
            while cluster_state not in ["WAITING"]:
                logging.info("Cluster is not ready yet. Current state={}. WIll check back in 15 secs.".format(cluster_state))
                time.sleep(15)
                cluster_state = self.session.compute_manager.get_cluster_status(cluster_id)
            logging.info("Cluster with id = {} is created.".format(cluster_id))
            response = self.session.compute_manager.submit_sql_step(cluster_id=cluster_id,
                                                                    sql_script=self.task_instance_executable,
                                                                    output_location=self.session.config_parser.sql_output_location,
                                                                    output_format=self.session.config_parser.sql_output_format)
            logging.debug("Response={}".format(response))
            return response
        except Exception:
            logging.error("Error occurred while executing workload.")
            raise


    def submit_task_to_cluster(self):
        return True

