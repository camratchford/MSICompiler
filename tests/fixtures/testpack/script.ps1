

$CWD = Split-Path -Parent $MyInvocation.MyCommand.Path
New-Item -Force -Path "$CWD\yes.txt" -value "1 2"

Add-Type -AssemblyName System.Windows.Forms
$global:Balloon = New-Object System.Windows.Forms.NotifyIcon
$Balloon.Icon = [System.Drawing.Icon]::new("$CWD\package-box.ico")
$Balloon.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Warning
$Balloon.BalloonTipText = "$cwd"
$Balloon.BalloonTipTitle = "Test from"
$Balloon.Visible = $true
$Balloon.ShowBalloonTip(10000)
