
param(
    $Var1,
    $Var2
)
$CWD = Split-Path -Parent $MyInvocation.MyCommand.Path
New-Item -Force -Path "$CWD\yes.txt" -value "$var1 $var2"