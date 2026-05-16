# Run this PowerShell script as Administrator on the Windows local machine.
# Purpose: allow Hermes VPS to access only approved local folders via OpenSSH over Tailscale.

$ErrorActionPreference = 'Stop'

# === CONFIG ===
$HermesUser = 'hermes'
$PublicKey = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILRVzspHoWhFz76uOA1T27l4yUfKQnoc8WfdYG5M5He+ hermes-vps-to-local'

# Folders Hermes is allowed to work in. Edit these paths if needed.
$AllowedFolders = @(
  'C:\HermesShared',
  "$env:USERPROFILE\Google Drive",
  "$env:USERPROFILE\My Drive",
  "$env:USERPROFILE\Google Drive\My Drive",
  "$env:USERPROFILE\Google Drive\Shared drives"
)

Write-Host 'Installing/starting OpenSSH Server...'
$cap = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
if ($cap.State -ne 'Installed') {
  Add-WindowsCapability -Online -Name $cap.Name
}
Set-Service -Name sshd -StartupType Automatic
Start-Service sshd

Write-Host 'Ensuring firewall rule for OpenSSH...'
if (-not (Get-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -ErrorAction SilentlyContinue)) {
  New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
}

Write-Host "Creating local user '$HermesUser' if missing..."
if (-not (Get-LocalUser -Name $HermesUser -ErrorAction SilentlyContinue)) {
  $Password = Read-Host "Set a strong temporary password for local user '$HermesUser'" -AsSecureString
  New-LocalUser -Name $HermesUser -Password $Password -Description 'Restricted account for Hermes VPS SSH access'
}

Write-Host 'Installing authorized SSH key...'
$UserProfile = "C:\Users\$HermesUser"
$SshDir = Join-Path $UserProfile '.ssh'
$AuthFile = Join-Path $SshDir 'authorized_keys'
New-Item -ItemType Directory -Force -Path $SshDir | Out-Null
Set-Content -Path $AuthFile -Value $PublicKey -Encoding ascii
icacls $SshDir /inheritance:r /grant "$HermesUser:(OI)(CI)F" /grant 'SYSTEM:(OI)(CI)F' /grant 'Administrators:(OI)(CI)F' | Out-Null
icacls $AuthFile /inheritance:r /grant "$HermesUser:F" /grant 'SYSTEM:F' /grant 'Administrators:F' | Out-Null

Write-Host 'Granting Modify permission on approved folders when they exist...'
foreach ($folder in $AllowedFolders) {
  if (Test-Path $folder) {
    Write-Host "Granting access: $folder"
    icacls $folder /grant "$HermesUser:(OI)(CI)M" | Out-Null
  } else {
    Write-Host "Skip missing folder: $folder"
  }
}

Write-Host 'Creating C:\HermesShared if missing...'
New-Item -ItemType Directory -Force -Path 'C:\HermesShared' | Out-Null
icacls 'C:\HermesShared' /grant "$HermesUser:(OI)(CI)M" | Out-Null

Write-Host ''
Write-Host 'DONE. Now send Doremon:'
Write-Host '1) The computer name you want to use from tailscale status, or its Tailscale IP.'
Write-Host '2) The exact Google Drive folder path on this PC.'
Write-Host '3) Confirmation that this script finished without errors.'
