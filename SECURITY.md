# Security

PC Remote lets a phone press keys and move the mouse on your computer, so it is built for a trusted home network:

- Only a phone holding the pairing key from the QR code can send commands. Anyone who sees the QR code or the link under it gets that key; issue a new one with `--reset-token`.
- Traffic is plain HTTP and is not encrypted. Do not expose the port (8765 by default) to the internet or use the remote on public Wi-Fi.

## Reporting a vulnerability

Please report security issues privately through [GitHub security advisories](https://github.com/universe-coder/mobile-pc-contoller/security/advisories/new) rather than a public issue.
