import msilib


from msi_compiler.msilib_util import get_custom_action


def sequence_custom_action(db, condition: str, action_id: str, sequence_id: int):
    # https://learn.microsoft.com/en-us/windows/win32/msi/sequence-table-detailed-example
    sequence_data = [(action_id, condition, sequence_id)]
    msilib.add_data(db, 'InstallExecuteSequence', sequence_data)
    msilib.add_data(db, 'AdminExecuteSequence', sequence_data)
    msilib.add_data(db, 'InstallUISequence', sequence_data)
    msilib.add_data(db, 'AdminUISequence', sequence_data)


def add_custom_install_action(db, action_id: str, action_type: int, source: str, target: str):
    # https://learn.microsoft.com/en-us/windows/win32/msi/custom-action-in-script-execution-options

    print(target)
    if get_custom_action(db, action_id):
        # raise FileExistsError(f"Custom action with id {action_id} already exists in the database")
        ...

    custom_action_data = [(action_id, action_type, source, target)]
    msilib.add_data(db, 'CustomAction', custom_action_data)
    db.Commit()


def add_powershell_install_action(db, condition: str, action_id: str, target: str, args: list[str]):
    # https://learn.microsoft.com/en-us/windows/win32/msi/custom-action-type-51
    action_type = 3106
    sequence_id = 6400
    arg_str = ""
    if args:
        arg_str = ", ".join([str(i) for i in args])

    powershell_path = r"[PowerShellPath]"
    start_process_line = f"start-process -FilePath PowerShell.exe -Wait -ArgumentList @('-WindowStyle Hidden', '-File {target}', {arg_str})"
    powershell_cli = f'{powershell_path} -NonInteractive -WindowStyle Hidden -NoLogo -NoProfile -Command "{start_process_line}"'
    source = f"TARGETDIR"
    add_custom_install_action(db, action_id, action_type, source, powershell_cli)
    sequence_custom_action(db, condition, action_id, sequence_id)

def add_executable_install_action(db, condition: str, action_id: str, target: str, args: list[str]):
    # https://learn.microsoft.com/en-us/windows/win32/msi/custom-action-type-34
    action_type = 34
    sequence_id = 6400
    arg_str = " ".join([str(i) for i in args])
    source = "TARGETDIR"
    add_custom_install_action(db, action_id, action_type, source, f'{target} {arg_str}')
    sequence_custom_action(db, condition, action_id, sequence_id)


ACTION_TYPES = {
    'powershell': add_powershell_install_action,
    'executable': add_executable_install_action
}