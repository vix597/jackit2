'''
Handles initial setup and tracking of useful globals
'''

import os
import sys
import logging

from jackit2.config import JackitConfig


class SiteDeploymentSingleton:
    '''
    Handles initial setup
    '''

    _instance = None

    @classmethod
    def instance(cls):
        '''
        Get instance of SiteDeploymentSingleton
        '''
        if cls._instance is None:
            cls._instance = SiteDeploymentSingleton()
            return cls._instance
        return cls._instance

    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.resource_path = os.path.join(self.base_path, "jackit2", "resources")
        self.config_path = os.path.join(self.base_path, "site.cfg.json")
        self._config = None
        self._setup_config()
        self._setup_logging()

    @property
    def config(self):
        '''
        Config getter
        '''
        return self._config

    def _setup_logging(self):
        '''
        Setup the root logger
        '''
        root_logger = logging.getLogger()

        if self.config.is_development_mode():
            root_logger.setLevel(logging.DEBUG)
            log_stdout_handler = logging.StreamHandler(sys.stdout)
            log_stdout_handler.setLevel(logging.DEBUG)
            root_logger.addHandler(log_stdout_handler)

    def _setup_config(self):
        '''
        Setup the config file
        '''
        self._config = JackitConfig(self.config_path)
        if os.path.exists(self.config_path):
            self._config.load()
        self._config.save()


SITE_DEPLOYMENT = SiteDeploymentSingleton.instance()