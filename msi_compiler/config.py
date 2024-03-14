import msilib
from pathlib import Path

import yaml

from msi_compiler.exceptions import ConfigPropertyError, ConfigPropertyWarning
from msi_compiler.types import PathProperties, NullableProperties, is_f_string_template


class Config:
    r"""
    Class to load and store configuration parameters.
    """
    source_folder: str = ""
    destination_folder: str = ""
    custom_install_actions: list[dict] = [{}]
    custom_uninstall_actions: list[dict] = [{}]
    msi_package_path: str = ""
    package_name: str = ""
    product_code: str = ""
    package_version: str = ""
    company: str = ""
    manufacturer: str = ""
    msi_properties = {}
    environment_variables: list[dict] = [{}]

    def __init__(self, **kwargs):
        if kwargs is None:
            raise ConfigPropertyError("Config cannot be empty")
        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise ConfigPropertyWarning(f"Config does not contain property '{k}', this will be ignored")
            if k and (not v and not isinstance(k, NullableProperties)):
                raise ConfigPropertyError(f"Config property '{k}' cannot be empty")

        self.__dict__.update(kwargs)
        self.format_string_attrs()
        self.setup()

    def format_string_attrs(self):
        r"""
        Processes class properties for strings that contain Python string.format() character '{'
        Replaces the format variable with the corresponding value from the class's __dict__ attribute.

        Example:
            # The input (YAML text read in by Config.from_file)
            package_name: 'TestPackage'
            package_version: '1.0.0'
            msi_package_path: 'C:\Users\Cam\MSICompiler\tests\{package_name}_{package_version}.msi'

            # Resulting class properties
            config.package_name = 'TestPackage'
            config.package_version = '1.0.0'
            config.msi_package_path = 'C:\Users\Cam\MSICompiler\tests\TestPackage_1.0.0.msi'
        """
        self.__dict__ = self.format_strings_in_dict(self.__dict__)
        self.msi_properties = self.format_strings_in_dict(self.msi_properties)
        self.custom_install_actions = [
            self.format_strings_in_dict(action) for action in self.custom_install_actions
        ]
        self.custom_uninstall_actions = [
            self.format_strings_in_dict(action) for action in self.custom_uninstall_actions
        ]

    def format_strings_in_dict(self, d: dict):
        """
        Processes a dictionary for strings that contain Python string.format() character '{',
        using the class's __dict__ as supplied values.
        If the property appears in msi_compiler.types.PathProperties, the value is converted to a Path object and resolved.
        :param d: The dictionary to process
        :return: The dictionary, after formatting any strings that contain Python string.format() character '{'
        """
        for k, v in d.items():
            if is_f_string_template(v):
                try:
                    v = v.format(**self.__dict__)
                except:
                    pass
            if k in PathProperties.__args__:
                v = str(Path(v).resolve())
            d[k] = v
        return d

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

    def setup(self):
        """
        Executes various setup tasks:
        - Creates the directory structure for outputs if it does not exist
        :return:
        """

        if not Path(self.destination_folder).exists():
            Path(self.destination_folder).mkdir(parents=True)



