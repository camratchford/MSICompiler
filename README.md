# MSICompiler

MSICompiler is a tool to create MSI packages for Windows. 
It is a simple tool that uses a configuration file to create the MSI package. 
It is written in Python and uses the `msilib` library to create the MSI package.


### [Download](https://github.com/camratchford/MSICompiler/releases/download/0.1.0/MSICompiler.zip)

## Features

- YAML-based configuration
- Placing a directory full of files into a specified location
- Executing a PowerShell script with arguments

## Limitations

- No GUI
- Not thoroughly tested, but it works on my machine!
- Many of the features that MSI packages support are not supported by MSICompiler
  - Registry keys
  - Services
  - Custom actions (that aren't the one powershell script you specify)
  - Uninstall actions

> See the Future Plans section for more features lacking in MSICompiler

## Usage

To use MSICompiler, you need to create a configuration file.

Below is a sample configuration file: 

### `config.yaml`

```yaml
# The source folder is the folder that contains the files to be packaged into the MSI
source_folder: 'C:\Users\Cam\MSICompiler\tests\testpack'
# The destination folder is the folder where the contents of the 'source_folder' will be copied to during the 'INSTALL' action
destination_folder: 'C:\Users\Cam\MSICompiler\tests\testdest'
# The powershell_script is the script that will be run during the 'INSTALL' action. This script must be located within the 'source_folder'
powershell_script: 'script.ps1'
# The 'script_args' are the arguments that will be passed to the 'powershell_script'. All values are later cast to strings
script_args:
  - 1
  - "2"
# The 'msi_package_path' is the path to the MSI package that will be created
msi_package_path: 'C:\Users\Cam\MSICompiler\tests\TestPackage_1.0.0.msi'

# The following parameters are used to set metadata for the MSI package.
# The parameters may be optional, but this is an assumption which has not been tested as of yet.
package_name: 'TestPackage'
package_version: '1.0.0'
company: 'RatchfordConsulting'
manufacturer: 'RatchfordManufacturing'
contact_email: 'camratchford@gmail.com'
webpage: 'https://support.ratchfordconsulting.com/'
upgrade_code: '{39CFB886-7C1D-4469-A9C1-0C578E1C36D8}'
```

To create the MSI package, you can use the following command:
```powershell
MSICompiler.exe -c "config.yaml"
```

To run the msi package, you can use the following command:
```powershell
# The full path must be provided if executing the MSI with msiexec
msiexec /i /qn "C:\Users\Cam\MSICompiler\tests\TestPackage_1.0.0.msi" -log "install.log"

# This method relies on file extension handlers, but it is generally safe to assume that .msi is mapped correctly
# Assumes that the msi package is in the current directory
./TestPackage_1.0.0.msi
```

## Future Plans

> Feel free to submit a feature request as an issue

- Uninstall actions
- Testing
- Additional script actions
- Executable actions
  - DLLs
  - EXEs
- Registry keys
- Scheduled tasks
- Services
- Appending to the PATH environment variable
- GUI