
import logging

from pathlib import Path

import msilib
import msilib.schema
import msilib.sequence

from msi_compiler.config import Config

logger = logging.getLogger(__name__)


def calculate_size(source_dir: str):
    """
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
    """
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
    """
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
    """
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


def add_powershell_script(db, script_name: str, script_args: list[str]):
    """
    Add a CustomAction and assoicated Sequence to their respective tables.
    The action will execute 'script_name' with its arguments 'script_args' in powershell.
    :param db:
    :param script_name:
    :param script_args:
    :return:
    """
    args = ""
    if script_args:
        args = " ".join([str(i) for i in script_args])

    type_ = 3106 # https://learn.microsoft.com/en-us/windows/win32/msi/custom-action-type-51
    pwsh_line = f'powershell.exe -c "[TARGETDIR]{script_name}" {args}'

    target = f"cmd.exe /C call {pwsh_line}"
    action_id = "SCRIPTRUN"
    customaction_data = [(action_id, type_, 'TARGETDIR', target)]
    msilib.add_data(db, 'CustomAction', customaction_data)
    db.Commit()


    sequence_id = 6400 # https://learn.microsoft.com/en-us/windows/win32/msi/installexecutesequence-table
    # ActionID, Condition (True), Sequence
    sequence_data = [(action_id, '1=1', sequence_id)]
    msilib.add_data(db, 'InstallExecuteSequence', sequence_data)


def create_msi(config: Config):
    """
    Creates an MSI package using the parameters contained in the config object
    :param config: A Config object
    :return:
    """

    # https://willpittman.net:8080/index.php?title=Python_msilib_basics
    source_folder = config.source_folder
    source_obj = Path(source_folder)
    destination_folder = config.destination_folder
    powershell_script = config.powershell_script
    script_args = config.script_args

    msi_package_path = config.msi_package_path
    package_name = config.package_name
    package_version = config.package_version
    company = config.company
    contact_email = config.contact_email
    webpage = config.webpage
    upgrade_code = config.upgrade_code

    db = msilib.init_database(
        msi_package_path,
        msilib.schema,
        package_name,
        msilib.gen_uuid(),
        package_version,
        company
    )

    msilib.add_tables(db, msilib.sequence)

    property_data = [
        ('ARPCONTACT', contact_email),
        ('ARPURLINFOABOUT', webpage),
        ('ARPSIZE', calculate_size(source_folder)),
        ('ARPREADME', f"{destination_folder}\\README.txt"),
        ('UpgradeCode', upgrade_code)
    ]

    msilib.add_data(db, 'Property', property_data)
    db.Commit()

    cab = msilib.CAB(package_name)
    dir_obj = add_directory(db, cab)
    set_target_dir(db, destination_folder)

    feature_id = "Everything"
    file_list = [i for i in source_obj.iterdir()]
    add_feature(db, cab, feature_id, dir_obj, file_list)
    add_powershell_script(db, powershell_script, script_args)
    db.Commit()
    db.Close()


