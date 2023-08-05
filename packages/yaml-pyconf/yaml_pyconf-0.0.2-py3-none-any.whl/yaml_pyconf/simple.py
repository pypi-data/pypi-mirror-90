import pathlib

from yaml_pyconf.base import BaseConfig


class SimpleConfig(BaseConfig):

    def __new__(
            cls,
            yaml_path=pathlib.Path(__file__).parent.joinpath("samples").joinpath("sample-yaml").joinpath("simple.yaml")
    ):
        return super(SimpleConfig, cls).__new__(cls, yaml_path)

    @classmethod
    def select_config(cls, conf):
        return super(SimpleConfig, cls).select_config(conf)

    @classmethod
    def set_dotenv_var_from_yaml_conf(cls, instance, conf, list_name=None):
        return super(SimpleConfig, cls).set_dotenv_var_from_yaml_conf(instance, conf)
