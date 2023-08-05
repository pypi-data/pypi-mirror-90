import yaml
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv


class BaseConfig(ABC):
    _instance = None

    def __new__(cls, yaml_path, dotenv_path=None):
        if cls._instance is None:

            if dotenv_path is None:
                load_dotenv()
            else:
                load_dotenv(dotenv_path)

            with open(yaml_path) as f:
                conf = cls.select_config(yaml.safe_load(f))

            instance = super(BaseConfig, cls).__new__(cls)
            for k, v in conf.items():
                instance.__setattr__(k, v)

            instance = cls.set_dotenv_var_from_yaml_conf(instance, conf)

            cls._instance = instance

        return cls._instance

    @classmethod
    @abstractmethod
    def select_config(cls, conf):
        """
        Add custom logic here to return only a subset of the config, e.g., "development"
        :param conf: dict of config k/v
        :return: The sub-dict from which you want to directly set attributes for the
            instance
        """
        return conf

    @classmethod
    @abstractmethod
    def set_dotenv_var_from_yaml_conf(cls, instance, conf, list_name=None):
        """Override w/default list name if desired. Non-op as-is"""
        if list_name is not None:
            if list_name in conf:
                for attribute in conf[list_name]:
                    instance.__setattr__(attribute, os.getenv(attribute))
        return instance

    @classmethod
    def destroy(cls):
        cls._instance = None