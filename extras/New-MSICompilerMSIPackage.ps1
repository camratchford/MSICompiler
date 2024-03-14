$CWD = Split-Path -Path $($MyInvocation.MyCommand.Source) -Parent
$ProjectRoot = Split-Path -Path $CWD -Parent
$MSICompilerPath = Join-Path -Path $ProjectRoot "dist/MSICompiler.exe"
$OutputPath = Join-Path -Path $ProjectRoot "package"
New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
Copy-Item -Path $MSICompilerPath -Destination $OutputPath -Force
Copy-Item -Path $CWD/package-box.ico -Destination $OutputPath -Force
Copy-Item -Path $ProjectRoot/README.md -Destination $OutputPath -Force

$MSICompilerConfig = Join-Path -Path $ProjectRoot "extras/package_msicompiler.yml"
$MSICompilerArgs = @(
    "-c $MSICompilerConfig"
)

Start-Process -Wait -NoNewWindow -FilePath $MSICompilerPath -ArgumentList $MSICompilerArgs
