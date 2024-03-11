
import logging

from pathlib import Path

import msilib
import msilib.schema
import msilib.sequence

from msi_compiler.config import Config
from msi_compiler.msilib_util import new_msilib_db
from msi_compiler.custom_actions import ACTION_TYPES

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


def create_msi(config: Config):
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
    package_version = config.package_version
    company = config.company
    property_data = config.properties
    property_data['ARPSIZE'] = calculate_size(source_folder)

    with new_msilib_db(msi_package_path, package_name, package_version, company) as db:
        msilib.add_tables(db, msilib.sequence)
        set_target_dir(db, destination_folder)

        for prop, value in property_data.items():
            add_property(db, prop, value)

        cab = msilib.CAB(package_name)
        dir_obj = add_directory(db, cab)


        feature_id = "Everything"
        file_list = [i for i in source_obj.iterdir()]
        add_feature(db, cab, feature_id, dir_obj, file_list)

        if config.custom_actions:
            for i, action in enumerate(config.custom_actions):
                action_type = action.get("type")
                if action_type in ACTION_TYPES:
                    ACTION_TYPES[action_type](db, i+1, action.get('name'), action.get('target'), action.get('args'))
                else:
                    # todo: raise custom warning
                    ...


