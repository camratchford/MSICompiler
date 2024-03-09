
from pathlib import Path
from msi_compiler.config import Config

config_dict = {
    "source_folder": str(Path(r".\fixtures\testpack").resolve()),
    "destination_folder": str(Path(r".\fixtures\testdest").resolve()),
    "powershell_script": "test.ps1",
    "script_args": [1, "2"],
    "msi_package_path": str(Path(r".\{package_name}_{package_version}.msi").resolve()),
    "package_name": "TestPackage",
    "package_version": "1.0.0",
    "company": "RatchfordConsulting",
    "manufacturer": "RatchfordManufacturing",
    "contact_email": "camratchford@gmail.com",
    "webpage": "https://support.ratchfordconsulting.com/",
    "upgrade_code": "{39CFB886-7C1D-4469-A9C1-0C578E1C36D8}",
}


def test_config_dict():
    config = Config(**config_dict)
    assert config.source_folder == str(Path(r".\fixtures\testpack").resolve())
    assert config.destination_folder == str(Path(r".\fixtures\testdest").resolve())
    assert config.powershell_script == "test.ps1"
    assert config.script_args == [1, "2"]
    assert config.msi_package_path == str(Path(r".\TestPackage_1.0.0.msi").resolve())
    assert config.package_version == "1.0.0"
    assert config.company == "RatchfordConsulting"
    assert config.manufacturer == "RatchfordManufacturing"
    assert config.contact_email == "camratchford@gmail.com"
    assert config.webpage == "https://support.ratchfordconsulting.com/"
    assert config.upgrade_code == "{39CFB886-7C1D-4469-A9C1-0C578E1C36D8}"
    assert config.package_name == "TestPackage"


def test_config_yaml():
    config_path = str(Path(r".\fixtures\config.yml").resolve())
    config = Config.from_file(config_path)
    assert config.source_folder == str(Path(r".\fixtures\testpack").resolve())
    assert config.destination_folder == str(Path(r".\fixtures\testdest").resolve())
    assert config.powershell_script == "script.ps1"
    assert config.script_args == [1, "2"]
    assert config.msi_package_path == str(Path(r".\TestPackage_1.0.0.msi").resolve())
    assert config.package_version == "1.0.0"
    assert config.company == "RatchfordConsulting"
    assert config.manufacturer == "RatchfordManufacturing"
    assert config.contact_email == "camratchford@gmail.com"
    assert config.webpage == "https://support.ratchfordconsulting.com/"
    assert config.upgrade_code == "{39CFB886-7C1D-4469-A9C1-0C578E1C36D8}"
    assert config.package_name == "TestPackage"