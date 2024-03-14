$CWD = Split-Path -Path $($MyInvocation.MyCommand.Source) -Parent
$ProjectRoot = Split-Path -Path $CWD -Parent
$VenvPath = Join-Path -Path $CWD "venv"

$PyInstallerArgs = @(
    "-y",
    "--clean",
    "--console",
    "--onefile",
    "--icon=$CWD\package-box.ico",
    "--name=MSICompiler.exe",
    "--paths=$ProjectRoot\msi_compiler",
#    "--collect-submodules=msi_compiler",
     "$ProjectRoot\cli.py"
)
$Args = $PyInstallerArgs -join " "

Invoke-Expression "$VenvPath\Scripts\activate"
Invoke-Expression "Pyinstaller $Args"