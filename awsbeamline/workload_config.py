import yaml
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%dT%H:%M:%S')

class WorkloadConfigParser:

    def __init__(self, job_config_file_location):
        self._job_config = yaml.load(job_config_file_location, Loader=yaml.FullLoader)
        self.job_type = self._job_config.get("kind")
        self._metadata = self._job_config.get("spec").get("metadata")
        self._compute = self._job_config.get("spec").get("compute")
        self._executable = self._job_config.get("spec").get("executable")
        self._environment = self._job_config.get("spec").get("environment")


    @property
    def  compute_size(self):
        return self._compute.get("size")

    @property
    def  compute_engine(self):
        return self._compute.get("engine")

    @property
    def  compute_engine_version(self):
        return self._compute.get("engineVersion")

    @property
    def  compute_param_set_name(self):
        return self._compute.get("paramSetName")

    @property
    def  job_name(self):
        return self._metadata.get("jobName")

    @property
    def  namespace(self):
        return self._metadata.get("namespace")

    @property
    def  priority(self):
        return self._metadata.get("priority")
    
    @property
    def executable_location(self):
        return self._executable.get("location")
    
    @property
    def sql_output_location(self):
        if self.job_type == "SQL":
            return self._executable.get("output").get("location")
        else:
            raise ValueError("Invalid parameter: sql_output_location for non SQL job.")
    
    @property
    def sql_output_format(self):
        if self.job_type == "SQL":
            return self._executable.get("output").get("format")
        else:
            raise ValueError("Invalid parameter: sql_output_format for non SQL job.")
    
