import os
import tempfile
import msilib
from pathlib import Path


from msi_compiler.compiler import (
    calculate_size,
    add_feature,
    add_directory,
    set_target_dir,
    add_property
)
from msi_compiler.custom_actions import add_powershel_action, add_executable_action
from msi_compiler.msilib_util import (
    get_feature,
    get_property,
    get_custom_action,
    get_directory,
    get_install_execute_sequence
)

from cleanup import cleanup
from msilib_objs import msilib_db


def test_calculate_size():
    # Create a temporary directory with some files
    with tempfile.TemporaryDirectory() as tmpdirname:
        file1 = os.path.join(tmpdirname, 'file1.txt')
        file2 = os.path.join(tmpdirname, 'file2.txt')
        with open(file1, 'w') as f:
            f.write('Hello, World!')
        with open(file2, 'w') as f:
            f.write('Hello, again!')

        size = calculate_size(tmpdirname)
        assert size == os.path.getsize(file1) + os.path.getsize(file2)


def test_add_feature():
    cleanup()
    with msilib_db('test.msi') as db:
        db = db
        cab = msilib.CAB('test')
        dir_obj = add_directory(db, cab)

        # Call the function
        file_list = Path(__name__).parent.joinpath("fixtures/testpack").iterdir()
        add_feature(db, cab, "Everything", dir_obj, [i for i in file_list])
        db_feature = get_feature(db, "Everything")
        assert db_feature.get("feature_parent") == ""
        assert db_feature.get("title") == "Everything"
        assert db_feature.get("description") == "Everything"
        assert db_feature.get("display") == "0"
        assert db_feature.get("level") == "1"
        assert db_feature.get("directory") == "TARGETDIR"



def test_add_directory():
    cleanup()
    with msilib_db('test.msi') as db:
        db = db
        cab = msilib.CAB('test')

        # Call the function
        dir_obj = add_directory(db, cab)

        assert isinstance(dir_obj, msilib.Directory)
        assert dir_obj.db == db
        assert dir_obj.cab == cab
        assert dir_obj.basedir == None
        assert dir_obj.physical == "."
        assert dir_obj.logical == "TARGETDIR"
        db_dir = get_directory(db, "TARGETDIR")
        assert db_dir.get("default_dir") == "SourceDir"
        assert db_dir.get("directory_parent") == ""


def test_set_target_dir():
    cleanup()
    target_dir = Path(__name__).parent.joinpath("fixtures/testdest")
    with msilib_db('test.msi') as db:
        db = db
        set_target_dir(db, str(target_dir))
        db_action = get_custom_action(db, "SetTargetDirAction")
        assert db_action.get("type") == "51"
        assert db_action.get("source") == "TARGETDIR"
        assert db_action.get("target") == str(target_dir)


def test_add_executable_action():
    cleanup()
    action_id = "RunTestScript"
    sequence_offset = 1
    target = "[System64Folder]\msg.exe"

    with msilib_db('test.msi') as db:
        db = db
        add_executable_action(db, sequence_offset, action_id, target, ["*", "Testing"])
        db_action = get_custom_action(db, action_id)
        assert db_action.get("type") == str(34 + 17920)
        db_sequence = get_install_execute_sequence(db, action_id)
        assert db_sequence.get("sequence_id") == str(sequence_offset + 1500)


def test_add_powershell_action():
    cleanup()
    action_id = "RunTestScript"
    sequence_offset = 2

    target = str(Path(__name__).parent.joinpath("outputs/testdest/test.ps1"))
    with msilib_db('test.msi') as db:
        db = db
        add_powershel_action(db, sequence_offset, action_id, target, ["1", "2"])
        db_action = get_custom_action(db, action_id)
        assert db_action.get("type") == str(51 + 17920)
        db_sequence = get_install_execute_sequence(db, action_id)
        assert db_sequence.get("sequence_id") == str(sequence_offset + 1500)


def test_add_property():
    cleanup()
    with msilib_db('test.msi') as db:
        db = db
        add_property(db, "TESTPROPERTY", "TESTVALUE")
        db_property = get_property(db, "TESTPROPERTY")
        assert db_property == "TESTVALUE"