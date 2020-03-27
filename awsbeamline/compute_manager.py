import os
import boto3
import logging
import importlib
from botocore.config import Config 

from awsbeamline.emr_config import EMRConfig

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%dT%H:%M:%S')



class ComputeManager():
    def __init__(self, session):
        """Manage the underlying compute infrastructure for ETL.
           A generic module that would support more than one type of compute environment

        Arguments:
            job_config_location {str} -- Location of job config file

        Raises:
            ValueError: Currently we support spark and presto workload on EMR. Value error is raised non EMR workloads.
        """
        self.session = session
        self.job_config = self.session.job_config
        if self.job_config.compute_engine in ["spark", "presto"]:
            self.compute_client = self.session.emr_session
            self.compute_config = EMRConfig(session=self.session, emr_config_file=os.environ["BEAMLINE_EMR_CONFIG_LOCATION"]
                                )
        else:
            raise ValueError("We currently suppport spark and presto workload on EMR only.")

    def start_compute(self):
        logging.info("Compute engine={}. An EMR cluster to be created".format(self.job_config.compute_engine))
        response = self.compute_client.create_cluster(
                cluster_name = self.job_config.compute_engine+"-"+self.job_config.compute_size+"-"+self.job_config.compute_param_set_name,
                logging_s3_path = self.compute_config.logging_s3_path,
                emr_release = self.compute_config.emr_release_label,
                subnet_id = self.compute_config.subnet_id,
                emr_ec2_role = self.compute_config.emr_ec2_role,
                emr_role=self.compute_config.emr_role,
                num_concurrent_steps = self.compute_config.num_concurrent_steps,
                ebs_root_volume_size = self.compute_config.ebs_root_volume_size,
                instance_type_master = self.compute_config.instance_type_master,
                instance_type_core = self.compute_config.instance_type_core,
                instance_type_task = self.compute_config.instance_type_task,
                instance_ebs_size_master = self.compute_config.instance_ebs_size_master,
                instance_ebs_size_core = self.compute_config.instance_ebs_size_core,
                instance_num_on_demand_master = self.compute_config.instance_num_on_demand_master,
                instance_ebs_size_task = self.compute_config.instance_ebs_size_task,
                instance_num_on_demand_core = self.compute_config.instance_num_on_demand_core,
                instance_num_on_demand_task = self.compute_config.instance_num_on_demand_task,
                instance_num_spot_master = self.compute_config.instance_num_spot_master,
                instance_num_spot_core = self.compute_config.instance_num_spot_core,
                instance_num_spot_task = self.compute_config.instance_num_spot_task,
                spot_bid_percentage_of_on_demand_master  = self.compute_config.spot_bid_percentage_of_on_demand_master,
                spot_bid_percentage_of_on_demand_core = self.compute_config.spot_bid_percentage_of_on_demand_core,
                spot_bid_percentage_of_on_demand_task = self.compute_config.spot_bid_percentage_of_on_demand_task,
                spot_provisioning_timeout_master = self.compute_config.spot_provisioning_timeout_master,
                spot_provisioning_timeout_core= self.compute_config.spot_provisioning_timeout_core,
                spot_provisioning_timeout_task= self.compute_config.spot_provisioning_timeout_task,
                spot_timeout_to_on_demand_master= self.compute_config.spot_timeout_to_on_demand_master,
                spot_timeout_to_on_demand_core= self.compute_config.spot_timeout_to_on_demand_core,
                spot_timeout_to_on_demand_task= self.compute_config.spot_timeout_to_on_demand_task,
                python3= self.compute_config.python3,
                spark_glue_catalog= self.compute_config.spark_glue_catalog,
                hive_glue_catalog= self.compute_config.hive_glue_catalog,
                presto_glue_catalog= self.compute_config.presto_glue_catalog,
                bootstraps_paths= self.compute_config.bootstraps_paths,
                debugging= self.compute_config.debugging,
                applications= self.compute_config.applications,
                visible_to_all_users= self.compute_config.visible_to_all_users,
                key_pair_name= self.compute_config.key_pair_name,
                security_group_master= self.compute_config.security_group_master,
                security_groups_master_additional= self.compute_config.security_groups_master_additional,
                security_group_slave=self.compute_config.security_group_slave,
                security_groups_slave_additional= self.compute_config.security_groups_slave_additional,
                security_group_service_access= self.compute_config.security_group_service_access,
                spark_log_level = "INFO",
                spark_jars_path = self.compute_config.spark_jars_path,
                spark_defaults = self.compute_config.spark_defaults,
                maximize_resource_allocation = self.compute_config.maximize_resource_allocation,
                steps= None,
                keep_cluster_alive_when_no_steps= self.compute_config.keep_cluster_alive_when_no_steps,
                termination_protected= self.compute_config.termination_protected,
                tags= self.compute_config.tags
            )
        return (response)

    def terminate_compute(self, job_flow_id: str):
        response = self.compute_client.terminate_compute(cluster_id=job_flow_id)
        return response

    def get_cluster_status(self, job_flow_id: str):
        response = self.compute_client.get_cluster_state(cluster_id=job_flow_id)
        return response
    
    def submit_sql_step(self, cluster_id: str, sql_script: str, output_location: str, output_format: str):
        response = self.compute_client.submit_sql_step(cluster_id=cluster_id, sql_script=sql_script, output_location=output_location, output_format=output_format)
        return response




#c = ComputeManager("config/examples/job_definition/spark_sql.yaml")
#c1 = c.start_compute()
#print(c1)
