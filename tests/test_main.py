import os
from time import sleep
from pathlib import Path
from subprocess import Popen, PIPE, run
from os import environ, getenv


from msi_compiler.config import Config
from msi_compiler.__main__ import main
from cleanup import cleanup

config_dict = {
    "source_folder": str(Path(r".\fixtures\testpack").resolve()),
    "destination_folder": str(Path(r".\outputs\testdest").resolve()),
    "custom_actions": [
        {
            "name": "TestAction1",
            "type": "powershell",
            "target": str(Path(r".\outputs\testdest\script.ps1").resolve()),
            "args": ["1", "2"]
        },
        {
            "name": "TestAction2",
            "type": "executable",
            "target": r"C:\Windows\System32\msg.exe",
            "args": ["*", "Test Message"]
        }
    ],

    "msi_package_path": str(Path(r".\outputs\{package_name}_{package_version}.msi").resolve()),
    "package_name": "TestPackage",
    "product_code": '{39CFB886-7C1D-4469-A9C1-0C578E1C36D8}',
    "package_version": "1.0.0",
    "company": "RatchfordConsulting",
    "manufacturer": "RatchfordManufacturing",
    "properties": {
        "ARPCONTACT": "camratchford@gmail.com",
        "ARPPRODUCTICON": r"{destination_folder}\package-box.ico",
        "ARPURLINFOABOUT": "https://support.ratchfordconsulting.com/",
        "ARPREADME": r"{destination_folder}\readme.txt",
        "UpgradeCode": "{39CFB886-7C1D-4469-A9C1-0C578E1C36D8}"
    },
    "environment_variables": [
        {
            "name": "MYAPP_HOME",
            "value": r"C:\Program Files\MyApp",
            "mode": "set"
        },
        {
            "name": "PATH",
            "value": r"C:\Program Files\MyApp",
            "mode": "append"
        },
        {
            "name": "DEPRECATED_MYAPP_VAR",
            "mode": "remove"
        }
    ]
}

def run_powershell(cmd: str):
    proc = run(
        executable=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
        args=[cmd],
        text=True,
        shell=True,
        stderr=PIPE,
        stdout=PIPE,
    )
    return proc.stdout


def get_user_env_var(var_name: str):
    return run_powershell(fr"Get-ItemPropertyValue -Path HKCU:\\environment -Name {var_name}").replace('\n', '')


def set_user_env_var(var_name: str, value: str):
    run_powershell(fr"Set-ItemProperty -Path HKCU:\\environment -Name {var_name} -Value {value}")


def test_install():
    outputs_path = str(Path(r".\outputs").resolve())
    run_powershell(rf"Remove-Item -Recurse -Force -Path {outputs_path}")
    config_path = str(Path(r".\fixtures\config.yml").resolve())
    config = Config.from_file(config_path)
    main(config)
    sleep(2)
    set_user_env_var('DEPRECATED_MYAPP_VAR', 'Obsolete Information')
    if Path(config.msi_package_path).exists():
        log_path = str(Path(r".\outputs\install.log").resolve())
        powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        msiexec_args = [f"{config.msi_package_path} /qn /log {log_path}"]
        p = Popen(executable=powershell_path, args=msiexec_args, text=True, shell=True, stdout=PIPE, stderr=PIPE)
        p.communicate()
        sleep(2)
        assert p.returncode == 0
        assert Path(log_path).exists()
        assert Path(config.destination_folder).joinpath('file1.txt').exists()
        assert Path(config.destination_folder).joinpath('yes.txt').exists()
        assert get_user_env_var('MYAPP_HOME') == r'C:\Program Files\MyApp'
        local_env_path = get_user_env_var('PATH').split(';')
        assert r'C:\Program Files\MyApp' in local_env_path
        assert get_user_env_var('DEPRECATED_MYAPP_VAR') == ''


def test_uninstall():
    run_powershell(r"Remove-Item -Recurse -Force -Path C:\Users\Cam\PycharmProjects\MSICompiler\tests\outputs")
    config_path = str(Path(r".\fixtures\config.yml").resolve())
    config = Config.from_file(config_path)
    app_guid = config.product_code
    msi_exec_path = r"C:\Windows\System32\msiexec.exe"
    log_path = str(Path(r".\outputs\uninstall.log").resolve())
    powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    destination_path = Path(config.destination_folder).resolve()
    msiexec_args = [f"{msi_exec_path} /X'{app_guid}' /qn /log {log_path}"]
    p = Popen(executable=powershell_path, args=msiexec_args, text=True, shell=True, stdout=PIPE, stderr=PIPE)
    p.communicate()
    assert p.returncode == 0
    assert not any([i.exists() for i in destination_path.iterdir()])

