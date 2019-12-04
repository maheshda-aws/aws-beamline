import yaml
import logging

logger = logging.getLogger(__name__)

class Config():

    def __init__(self, config_location):
        self._config_location = config_location
        self.job_config = yaml.parse()



