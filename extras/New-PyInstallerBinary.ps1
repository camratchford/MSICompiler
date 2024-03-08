$CWD = Split-Path -Path $($MyInvocation.MyCommand.Source) -Parent
$ProjectRoot = Split-Path -Path $CWD -Parent
$VenvPath = Join-Path -Path $ProjectRoot ".venv"

$PyInstallerArgs = @(
    "-y",
    "--clean",
    "--console",
    "--onefile",
    "--icon=$CWD\installer_icon.png",
    "--name=MSICompiler.exe",
    "--paths=$ProjectRoot\msi_compiler",
    "--collect-submodules=msi_compiler",
     "$ProjectRoot\cli.py"
)

write-host "$VenvPath\Scripts\Pyinstaller.exe"

Start-Process -Wait -NoNewWindow -FilePath "$VenvPath\Scripts\Pyinstaller.exe" -ArgumentList $PyInstallerArgs