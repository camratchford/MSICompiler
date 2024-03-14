

from typing import Literal

PathProperties = Literal[
    "source_folder",
    "destination_folder",
    "msi_package_path",
    "target",
    "ARPPRODUCTICON",
    "ARPREADME"
]

NullableProperties = Literal[
    'custom_install_actions',
    'custom_uninstall_actions',
    'environment_variables',
    'msi_properties'
]

def is_f_string_template(s: str) -> bool:
    return isinstance(s, str) and "{" in s and "}" in s