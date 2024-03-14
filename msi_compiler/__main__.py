
import msilib
import msilib.sequence

from pathlib import Path

from msi_compiler.config import Config
from msi_compiler.msilib_util import new_msilib_db
from msi_compiler.custom_actions import ACTION_TYPES
from msi_compiler.database_data import (
    calculate_size,
    add_property,
    set_target_dir,
    add_directory,
    add_feature,
    add_environment_variable_action
)


def main(config: Config):
    r"""
    Creates an MSI package using the parameters contained in the config object
    :param config: A Config object
    :return:
    """

    # https://willpittman.net:8080/index.php?title=Python_msilib_basics
    source_folder = config.source_folder
    source_obj = Path(source_folder)
    destination_folder = config.destination_folder

    msi_package_path = config.msi_package_path
    package_name = config.package_name
    product_code = config.product_code
    package_version = config.package_version
    company = config.company
    property_data = config.msi_properties
    property_data['ARPSIZE'] = calculate_size(source_folder)
    property_data['PowerShellPath'] = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'

    with new_msilib_db(msi_package_path, package_name, product_code, package_version, company) as db:
        msilib.add_tables(db, msilib.sequence)
        for prop, value in property_data.items():
            add_property(db, prop, value)

        cab = msilib.CAB(package_name)
        dir_obj = add_directory(db, cab)
        set_target_dir(db, destination_folder)

        feature_id = "Everything"
        file_list = [i for i in source_obj.iterdir()]
        add_feature(db, cab, feature_id, dir_obj, file_list)
        if config.custom_install_actions:
            for i, action in enumerate(config.custom_install_actions):
                action_type = action.get("type")
                if action_type in ACTION_TYPES:
                    ACTION_TYPES[action_type](db, "NOT REMOVE", action.get('name'), action.get('target'), action.get('args'))
                else:
                    # todo: raise custom warning
                    ...
        if config.custom_uninstall_actions:
            for i, action in enumerate(config.custom_uninstall_actions):
                action_type = action.get("type")
                if action_type in ACTION_TYPES:
                    ACTION_TYPES[action_type](db, "REMOVE", action.get('name'), action.get('target'), action.get('args'))
                else:
                    # todo: raise custom warning
                    ...
        if config.environment_variables:
            for env_var in config.environment_variables:
                add_environment_variable_action(
                    db,
                    env_var.get('name'),
                    env_var.get('value'),
                    env_var.get('mode'),
                    env_var.get('delimiter')
                )