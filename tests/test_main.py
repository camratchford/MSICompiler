
from time import sleep
from pathlib import Path
from subprocess import Popen, PIPE


from msi_compiler.config import Config
from msi_compiler.__main__ import main

config_dict = {
    "source_folder": str(Path(r".\fixtures\testpack").resolve()),
    "destination_folder": str(Path(r".\outputs\testdest").resolve()),
    "powershell_script": "test.ps1",
    "script_args": [1, "2"],
    "msi_package_path": str(Path(r".\outputs\{package_name}_{package_version}.msi").resolve()),
    "package_name": "TestPackage",
    "package_version": "1.0.0",
    "company": "RatchfordConsulting",
    "manufacturer": "RatchfordManufacturing",
    "contact_email": "camratchford@gmail.com",
    "webpage": "https://support.ratchfordconsulting.com/",
    "upgrade_code": "{39CFB886-7C1D-4469-A9C1-0C578E1C36D8}",
}


def test_main():
    config = Config(**config_dict)
    main(config)
    assert Path(config.msi_package_path).exists()


def test_install():
    config_path = str(Path(r".\fixtures\config.yml").resolve())
    config = Config.from_file(config_path)
    main(config)
    sleep(2)
    if Path(config.msi_package_path).exists():
        log_path = str(Path(r".\outputs\install.log").resolve())
        powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        msiexec_args = [f"{config.msi_package_path} /qn /log {log_path}"]
        p = Popen(executable=powershell_path, args=msiexec_args, text=True, shell=True, stdout=PIPE, stderr=PIPE)
        p.communicate()
        sleep(2)
        assert p.returncode == 0
        assert Path(log_path).exists()
        assert Path(config.destination_folder).exists()
        assert Path(config.destination_folder).joinpath('yes.txt')


