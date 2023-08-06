import os
import pathlib

from yaml_pyconf.base import BaseConfig


class FlaskConfig(BaseConfig):
    _db_uri = None

    def __new__(
            cls,
            yaml_path=None,
            dotenv_path=None,
    ):
        if not cls._instance:
            if yaml_path == "sample":
                yaml_path = pathlib.Path(__file__).parent.joinpath("samples").\
                                joinpath("sample-yaml").joinpath("flask-choose-env.yaml")

            if dotenv_path == "sample":
                dotenv_path = pathlib.Path(__file__).parent.joinpath("samples").\
                                  joinpath("sample-dotenv").joinpath(".env")

            if yaml_path is None:
                # search for path in calling app base path
                app_yaml_default = pathlib.Path("config.yaml")

                if not app_yaml_default.exists():
                    raise NotImplementedError("No config.yaml exists in your project "
                                              "directory. Please pass an explicit path "
                                              "to a correctly-formatted .yaml file for "
                                              "the 'yaml_path' argument, or use 'sample"
                                              "' to use the example config")
                yaml_path = app_yaml_default

        return super(FlaskConfig, cls).__new__(
            cls, yaml_path=yaml_path, dotenv_path=dotenv_path
        )

    @classmethod
    def select_config(cls, conf):
        conf = super(FlaskConfig, cls).select_config(conf)
        env = os.getenv("FLASK_ENV")
        if env is not None:
            try:
                conf = conf[env]
                return conf
            except KeyError:
                raise NotImplementedError("The value set for 'FLASK_ENV' attribute "
                                          "must match a section in your yaml config")
        else:
            raise NotImplementedError("You must set a variable called 'FLASK_ENV', "
                                      "in your .env or by using "
                                      "'export FLASK_ENV={yourEnvValue}, and "
                                      "{yourEnvValue} must match a section in your yaml "
                                      "file. If this doesn't make sense for your "
                                      "project, use SimpleConfig instead")

    @classmethod
    def set_dotenv_var_from_yaml_conf(cls, instance, conf, list_name="LOAD_FROM_ENV"):
        return super(FlaskConfig, cls).set_dotenv_var_from_yaml_conf(
            instance,
            conf,
            list_name=list_name
        )

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """
        Currently only supports SQLite and PostgreSQL.
        :return:
        """
        if self._db_uri is None:
            if self.DB_PREFIX == "sqlite:///":
                if "SQLITE_PROJECT_DIRECTORY" not in self.__dict__.keys():
                    # If there is no hardcoded path to SQLite DB parent in the env, put
                    # DB in the current directory
                    self.__setattr__(
                        "SQLITE_PROJECT_DIRECTORY",
                        str(pathlib.Path(".").absolute())
                    )
                self._db_uri = f"{self.DB_PREFIX}" \
                               f"{os.path.join(self.SQLITE_PROJECT_DIRECTORY, self.DB_NAME)}"

            elif self.DB_PREFIX == "postgresql://":
                self._db_uri = f"{self.DB_PREFIX}{self.DB_USERNAME}:{self.DB_PASSWORD}@" \
                       f"{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}"

        return self._db_uri
