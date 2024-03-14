
import logging

from pathlib import Path

import msilib
import msilib.schema
import msilib.sequence


logger = logging.getLogger(__name__)


def calculate_size(source_dir: str):
    r"""
    Returns a sum of the files contained within 'source_dir'
    :param source_dir:
    :return:
    """
    total_size = 0
    for file in Path(source_dir).iterdir():
        total_size += file.stat().st_size.real

    return round(total_size, 2)


def add_feature(
        db: msilib.OpenDatabase,
        cab_obj: msilib.CAB,
        feature_id: str,
        dir_obj: msilib.Directory,
        file_list: list[Path]
):
    r"""
    Sets a 'Feature', which is used to assoicate with files in 'dir_obj'.
    Adds files in 'file_list' to the 'cab_obj' file, and associates the cab with 'dir_obj'.
    :param db:
    :param cab_obj:
    :param feature_id:
    :param dir_obj:
    :param file_list:
    :return:
    """
    feature = msilib.Feature(
        db,
        feature_id,  # id
        feature_id,  # title
        feature_id,  # desc
        display=0,
        level=1,
        directory='TARGETDIR'
    )

    for file in file_list:
        feature.set_current()
        # noinspection PyTypeChecker
        dir_obj.add_file(file)

    db.Commit()
    cab_obj.commit(db)


# noinspection PyTypeChecker
def add_directory(
        db: msilib.OpenDatabase,
        cab_obj: msilib.CAB,
):
    r"""
    Add a directory
    :param db: The MSI database
    :param cab_obj: A msilib.CAB object, unique to each entry in the Directory table
    :param source_dir_id: The Directory table primary key of the parent directory of the directory you're creating
    :return: dir_obj: msilib.Directory (required argument in add_feature)
    """
    dir_obj = msilib.Directory(
        db,
        cab_obj,
        None,
        '.',
        'TARGETDIR',
        'SourceDir'
    )


    return dir_obj


def set_target_dir(db, target_dir: str):
    r"""
    Sets the TARGETDIR property, and adds the SetTargetDirAction to unpack the directory 'SourceDir' into 'target_dir'
    :param db: The MSI database
    :param target_dir: The directory in which the source directory will be placed as part of the 'INSTALL' action
    :return:
    """
    ...
    action_data = [(
        'SetTargetDirAction',
        51,
        'TARGETDIR',
        target_dir
    )]
    msilib.add_data(db, 'CustomAction', action_data)
    db.Commit()

    execute_data = [(
        'SetTargetDirAction',
         'Not TARGETDIR Or TARGETDIR=ROOTDRIVE',
         990
    )]
    msilib.add_data(db, 'InstallExecuteSequence', execute_data)
    msilib.add_data(db, 'AdminExecuteSequence', execute_data)
    msilib.add_data(db, 'InstallUISequence', execute_data)
    msilib.add_data(db, 'AdminUISequence', execute_data)
    db.Commit()


def add_property(db, property_id: str, value: str):
    r"""
    Adds a property to the MSI database
    :param db: The MSI database
    :param property_id: The property name
    :param value: The property value
    :return:
    """
    property_data = [(property_id, value)]
    msilib.add_data(db, 'Property', property_data)
    db.Commit()


def add_component(db, component_id: str, feature_id: str):
    # https://learn.microsoft.com/en-us/windows/win32/msi/component-table
    # Create component in component table

    # https://learn.microsoft.com/en-us/windows/win32/msi/writeenvironmentstrings-action
    component_guid = msilib.gen_uuid()
    condition = "NOT REMOVE"
    component_data = [(
        component_id,
        component_guid,
        "TARGETDIR",
        0,
        condition,
        None
    )]
    msilib.add_data(db, 'Component', component_data)
    db.Commit()

    # https://learn.microsoft.com/en-us/windows/win32/msi/featurecomponents-table
    # Add component to the FeatureComponents table
    feature_component_data = [(
        feature_id,
        component_id,
    )]
    msilib.add_data(db, 'FeatureComponents', feature_component_data)
    db.Commit()

    # https://learn.microsoft.com/en-us/windows/win32/msi/publishcomponent-table
    # Add component to the PublishComponent table
    # 1033, english
    publish_component_data = [(
        component_guid,
        1033,
        component_id,
        None,
        feature_id
    )]
    msilib.add_data(db, 'PublishComponent', publish_component_data)
    db.Commit()


def add_environment_variable_action(
        db,
        name: str,
        value: str = "",
        mode: str = "add",
        delimiter: str = ";"
):
    """
    Adds a custom action to set an environment variable
    :param db:
    :param name:
    :param value:
    :param mode:
    :param :delimiter:
    :return:
    """

    # https://learn.microsoft.com/en-us/windows/win32/msi/environment-table
    # Create environment variable in Environment table
    name_map = {
        "set": f"={name}",
        "append": f"={name}",
        "remove": f"-{name}"
    }
    value_map = {
        "set": f"{value}",
        "append": f"{value}{delimiter}[~]",
        "remove": f"{value}"
    }
    component_id = f"ENV_{name}_Component"
    feature_id = "Everything"
    add_component(db, component_id, feature_id)
    property_data = [(f"ENV_{name}*", name_map.get(mode), value_map.get(mode), component_id)]
    msilib.add_data(db, 'Environment', property_data)
    db.Commit()





