
from pathlib import Path
from msi_compiler.config import Config

config_dict_paths_expanded = {
    "source_folder": str(Path(r".\fixtures\testpack").resolve()),
    "destination_folder": str(Path(r".\outputs\testdest").resolve()),
    "custom_install_actions": [
        {
            "name": "TestInstallAction1",
            "type": "powershell",
            "target": str(Path(r".\outputs\testdest\script.ps1").resolve()),
            "args": [1, 2]
        },
        {
            "name": "TestInstallAction2",
            "type": "executable",
            "target": r"C:\Windows\System32\msg.exe",
            "args": ["*", "Test Message"]
        }
    ],
    "custom_uninstall_actions": [
        {
            "name": "TestUninstallAction1",
            "type": "executable",
            "target": r"C:\Windows\System32\msg.exe",
            "args": ["*", "Uninstall Test Message"]
        }
    ],

    "msi_package_path": r".\outputs\{package_name}_{package_version}.msi",
    "package_name": "TestPackage",
    "package_version": "1.0.0",
    "company": "RatchfordConsulting",
    "manufacturer": "RatchfordManufacturing",
    "msi_properties": {
        "ARPCONTACT": "camratchford@gmail.com",
        "ARPPRODUCTICON": str(Path(r".\outputs\testdest\package-box.ico").resolve()),
        "ARPURLINFOABOUT": "https://support.ratchfordconsulting.com/",
        "ARPREADME": str(Path(r".\outputs\testdest\README.txt").resolve()),
        "UpgradeCode": "{39CFB886-7C1D-4469-A9C1-0C578E1C36D8}"
    },
    "environment_variables": [
        {
            "name": "MYAPP_HOME",
            "value": r"C:\Program Files\MyApp",
            "mode": "set",
            "delimiter": ";",
        },
        {
            "name": "PATH",
            "value": r"C:\Program Files\MyApp",
            "mode": "append",
        },
        {
            "name": "DEPRECATED_MYAPP_VAR",
            "mode": "remove",
        }
    ]
}

config_dict = {
    "source_folder": r".\fixtures\testpack",
    "destination_folder": r".\outputs\testdest",
    "custom_install_actions": [
        {
            "name": "TestInstallAction1",
            "type": "powershell",
            "target": str(Path(r".\outputs\testdest\script.ps1").resolve()),
            "args": [1, 2]
        },
        {
            "name": "TestInstallAction2",
            "type": "executable",
            "target": r"C:\Windows\System32\msg.exe",
            "args": ["*", "Test Message"]
        }
    ],
    "custom_uninstall_actions": [
        {
            "name": "TestUninstallAction1",
            "type": "executable",
            "target": r"C:\Windows\System32\msg.exe",
            "args": ["*", "Uninstall Test Message"]
        }
    ],
    "msi_package_path": str(Path(r".\outputs\{package_name}_{package_version}.msi").resolve()),
    "package_name": "TestPackage",
    "package_version": "1.0.0",
    "company": "RatchfordConsulting",
    "manufacturer": "RatchfordManufacturing",
    "msi_properties": {
        "ARPCONTACT": "camratchford@gmail.com",
        "ARPPRODUCTICON": str(Path(r".\outputs\testdest\package-box.ico").resolve()),
        "ARPURLINFOABOUT": "https://support.ratchfordconsulting.com/",
        "ARPREADME": str(Path(r".\outputs\testdest\README.txt").resolve()),
        "UpgradeCode": "{39CFB886-7C1D-4469-A9C1-0C578E1C36D8}"
    },
    "environment_variables": [
        {
            "name": "MYAPP_HOME",
            "value": r"C:\Program Files\MyApp",
            "mode": "set",
            "delimiter": ";",
        },
        {
            "name": "PATH",
            "value": r"C:\Program Files\MyApp",
            "mode": "append",
        },
        {
            "name": "DEPRECATED_MYAPP_VAR",
            "mode": "remove"
        },
    ]
}


def test_config_dict():
    config = Config(**config_dict_paths_expanded)
    assert config.source_folder == str(Path(r".\fixtures\testpack").resolve())
    assert config.destination_folder == str(Path(r".\outputs\testdest").resolve())
    assert config.custom_install_actions == config_dict_paths_expanded.get('custom_install_actions')
    assert config.custom_uninstall_actions == config_dict_paths_expanded.get('custom_uninstall_actions')
    assert config.msi_package_path == str(Path(r".\outputs\TestPackage_1.0.0.msi").resolve())
    assert config.package_version == "1.0.0"
    assert config.company == "RatchfordConsulting"
    assert config.manufacturer == "RatchfordManufacturing"
    assert config.msi_properties == config_dict_paths_expanded.get('msi_properties')
    assert config.package_name == "TestPackage"


def test_config_yaml():
    config_path = str(Path(r".\fixtures\config.yml").resolve())
    config = Config.from_file(config_path)
    assert config.source_folder == str(Path(r".\fixtures\testpack").resolve())
    assert config.destination_folder == str(Path(r".\outputs\testdest").resolve())
    assert config.custom_install_actions == config_dict_paths_expanded.get('custom_install_actions')
    assert config.custom_uninstall_actions == config_dict_paths_expanded.get('custom_uninstall_actions')
    assert config.msi_package_path == str(Path(r".\outputs\TestPackage_1.0.0.msi").resolve())
    assert config.package_version == "1.0.0"
    assert config.company == "RatchfordConsulting"
    assert config.manufacturer == "RatchfordManufacturing"
    assert config.msi_properties == config_dict_paths_expanded.get('msi_properties')
    assert config.package_name == "TestPackage"