
from pathlib import Path

import yaml

from msi_compiler.exceptions import ConfigPropertyError, ConfigPropertyWarning


class Config:
    r"""
    Class to load and store configuration parameters.
    """
    source_folder: str = ""
    destination_folder: str = ""
    powershell_script: str = ""
    script_args: list = []
    msi_package_path: str = ""
    package_name: str = ""
    package_version: str = ""
    company: str = ""
    manufacturer: str = ""
    contact_email: str = ""
    webpage: str = ""
    upgrade_code: str = '{39CFB886-7C1D-4469-A9C1-0C578E1C36D8}'
    path_attrs = [
        "source_folder",
        "destination_folder",
        "msi_package_path",
    ]

    def __init__(self, **kwargs):
        if kwargs is None:
            raise ConfigPropertyError("Config cannot be empty")

        if not all(kwargs.values()):
            raise ConfigPropertyError("All configuration values must be specified")

        self.__dict__.update(kwargs)
        self.format_string_attrs()
        self.make_paths_absolute()

    def make_paths_absolute(self):
        r"""
        Converts relative paths to absolute paths
        """
        for attr, value in self.__dict__.items():
            try:
                if attr in self.path_attrs and not Path(value).is_absolute():
                    self.__dict__[attr] = str(Path(value).resolve())
            except Exception as e:
                # Some of these things aren't paths, and that's okay
                ...

    def format_string_attrs(self):
        r"""
        Processes class attributes for strings that contain Python string.format() character '{'
        Replaces the format variable with the corresponding value from the class's __dict__ attribute.

        Example:
            # The input (YAML text read in by Config.from_file)
            package_name: 'TestPackage'
            package_version: '1.0.0'
            msi_package_path: 'C:\Users\Cam\MSICompiler\tests\{package_name}_{package_version}.msi'

            # Resulting class attributes
            config.package_name = 'TestPackage'
            config.package_version = '1.0.0'
            config.msi_package_path = 'C:\Users\Cam\MSICompiler\tests\TestPackage_1.0.0.msi'
        """
        for attr, value in self.__dict__.items():
            if isinstance(value, str) and '{' in value:
                try:
                    self.__dict__[attr] = value.format(**self.__dict__)
                except Exception as e:
                    # We don't care if it works for everything
                    ...

    @classmethod
    def from_dict(cls, config_dict: dict):
        r"""
        Create a Config object from a dictionary containing configuration parameters
        :param config_dict: A dict object containing all configuration parameters
        :return: An instantiated Config object populated with the properties contained in the config_dict object
        """
        config = cls(**config_dict)
        return config

    @classmethod
    def from_file(cls, config_file):
        r"""
        Create a Config object from a YAML config file
        :param config_file: A path string where the yaml config file resides
        :return: An instantiated Config object populated with the properties contained in the config file
        """
        config_file_path = Path(config_file).resolve()
        config_dict = dict()
        if config_file_path.exists() and (
            ".yml" in config_file_path.suffixes
            or (".yaml" in config_file_path.suffixes)
        ):
            with open(config_file, "r") as file:
                loaded_config = yaml.safe_load(file)

            if not loaded_config:
                raise ConfigPropertyError("Config file must not be empty")
            for attr, prop in loaded_config.items():
                if not cls.__dict__.__contains__(attr):
                    raise ConfigPropertyWarning(f"Config does not contain property '{attr}', this will be ignored")

                config_dict[attr] = prop

            return cls.from_dict(config_dict)
        raise ConfigPropertyError(f"Config file [{config_file_path}] not found or invalid extension used")


