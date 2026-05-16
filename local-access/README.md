# Hermes VPS → Local PC access

## Current VPS state
- Tailscale installed and connected.
- SSH client installed.
- SSH key created: `/root/.ssh/hermes_local_ed25519`.
- Public key:

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILRVzspHoWhFz76uOA1T27l4yUfKQnoc8WfdYG5M5He+ hermes-vps-to-local
```

## Known Tailscale peers from VPS
- `desktop-ae5jd4o` — `100.82.200.42` — Windows — online, SSH port not open yet.
- `ha` — `100.94.184.101` — Windows — online, SSH connection refused.
- `desktop-tang-3` — `100.82.196.3` — Windows — offline at setup time.

## Next steps
1. On the Windows PC that should expose Google Drive/local folders, run PowerShell as Administrator.
2. Copy and run `setup_windows_ssh_hermes.ps1`.
3. Send back the chosen PC name/IP and exact Google Drive local path.
4. Test from VPS:

```bash
ssh -i /root/.ssh/hermes_local_ed25519 -o IdentitiesOnly=yes hermes@<tailscale-ip-or-hostname>
```

5. If successful, create SSH config alias:

```sshconfig
Host anh-local
  HostName <tailscale-ip-or-hostname>
  User hermes
  IdentityFile /root/.ssh/hermes_local_ed25519
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 3
```

## Safety policy
- Only grant the `hermes` Windows user Modify permission to approved folders.
- Do not grant full disk/admin access unless explicitly approved.
- Deleting/moving files still requires Boss approval.
