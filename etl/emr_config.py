import yaml
import logging

emr_config_file =  "emr.yaml"

class EMRConfig:

    def __init__(self, cluster_size, app_name, app_version, param_set_name):
        self._emr_config = yaml.load(open(emr_config_file), Loader=yaml.FullLoader).get("spec")
        self._cluster_size = cluster_size
        self._app_name = app_name
        self._app_version = app_version
        self._param_set_name = param_set_name
        self._cluster_size_config = self.emr_config["clusterSize"].get(self._cluster_size)
        self._emr_release_label = self.emr_config["appVersion"].get(self._app_name).get(self._app_version)
        self._cluster_parameters = self.emr_config["clusterParamSet"].get(self._param_set_name)

    @property
    def  instance_type_master(self):
        return self._cluster_size_config.get("instance_type_master")

    @property
    def  instance_num_on_demand_master(self):
        return self._cluster_size_config.get("instance_num_on_demand_master")

    @property
    def  instance_num_spot_master(self):
        return self._cluster_size_config.get("instance_num_spot_master")

    @property
    def  instance_ebs_size_master(self):
        return self._cluster_size_config.get("instance_ebs_size_master")

    @property
    def  spot_bid_percentage_of_on_demand_master(self):
        return self._cluster_size_config.get("spot_bid_percentage_of_on_demand_master")

    @property
    def  instance_type_core(self):
        return self._cluster_size_config.get("instance_type_core")

    @property
    def  instance_num_on_demand_core(self):
        return self._cluster_size_config.get("instance_num_on_demand_core")

    @property
    def  instance_num_spot_core(self):
        return self._cluster_size_config.get("instance_num_spot_core")

    @property
    def  instance_ebs_size_core(self):
        return self._cluster_size_config.get("instance_ebs_size_core")

    @property
    def  spot_bid_percentage_of_on_demand_core(self):
        return self._cluster_size_config.get("spot_bid_percentage_of_on_demand_core")

    @property
    def  instance_type_task(self):
        return self._cluster_size_config.get("instance_type_task")

    @property
    def  instance_num_on_demand_task(self):
        return self._cluster_size_config.get("instance_num_on_demand_task")

    @property
    def  instance_num_spot_task(self):
        return self._cluster_size_config.get("instance_num_spot_task")

    @property
    def  instance_ebs_size_task(self):
        return self._cluster_size_config.get("instance_ebs_size_task")

    @property
    def  spot_bid_percentage_of_on_demand_task(self):
        return self._cluster_size_config.get("spot_bid_percentage_of_on_demand_task")

    @property
    def emr_release_label(self):
        return self._emr_release_label

    @property
    def logging_s3_path(self):
        return self._param_set_name.get("logging_s3_path")

    @property
    def subnet_id(self):
        return self._param_set_name.get("subnet_id")

    @property
    def emr_ec2_role(self):
        return self._param_set_name.get("emr_ec2_role")

    @property
    def emr_role(self):
        return self._param_set_name.get("emr_role")

    @property
    def spot_timeout_to_on_demand_master(self):
        return self._param_set_name.get("spot_timeout_to_on_demand_master")

    @property
    def spot_timeout_to_on_demand_core(self):
        return self._param_set_name.get("spot_timeout_to_on_demand_core")

    @property
    def spot_timeout_to_on_demand_task(self):
        return self._param_set_name.get("spot_timeout_to_on_demand_task")

    @property
    def spark_glue_catalog(self):
        return self._param_set_name.get("spark_glue_catalog")

    @property
    def application(self):
        return self._param_set_name.get("application")


#e = EMRConfig("XL", "spark", "2.4.4", "default")
#print(e.config_file)