
from pathlib import Path

from msi_compiler.custom_actions import add_executable_action, add_powershell_action
from cleanup import cleanup
from msilib_objs import msilib_db

from msi_compiler.msilib_util import (
    get_custom_action,
    get_install_execute_sequence,
)


def test_add_executable_action():
    cleanup()
    action_id = "RunTestScript"
    target = "[System64Folder]\msg.exe"

    with msilib_db('test.msi') as db:
        db = db
        add_executable_action(db, action_id, target, ["*", "Testing"])
        db_action = get_custom_action(db, action_id)
        assert db_action.get("type") == str(34)
        db_sequence = get_install_execute_sequence(db, action_id)
        assert db_sequence.get("sequence_id") == str(6400)


def test_add_powershell_action():
    cleanup()
    action_id = "RunTestScript"

    target = str(Path(__name__).parent.joinpath("outputs/testdest/test.ps1"))
    with msilib_db('test.msi') as db:
        db = db
        add_powershell_action(db, action_id, target, ["1", "2"])
        db_action = get_custom_action(db, action_id)
        assert db_action.get("type") == str(3106)
        db_sequence = get_install_execute_sequence(db, action_id)
        assert db_sequence.get("sequence_id") == str(6400)

