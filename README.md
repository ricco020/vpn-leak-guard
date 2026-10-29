# VPN Leak Guard: WebRTC & IP Leak Test (Chrome extension)

One click tells you whether your VPN really hides your IP:

- **Public IP** as websites see it (ISP, location).
- **WebRTC** candidates gathered through STUN, compared with the public IP: a mismatch is a leak.
- **Timezone** consistency between the browser and the IP.
- **Block WebRTC leaks** toggle (sets Chrome's `webRTCIPHandlingPolicy` to `disable_non_proxied_udp`).
- **Home IP**: save your real IP once, and the guard can prove the VPN hides it.
- **DNS leak test** (since 1.0.2): lists the DNS resolvers your browser really uses, through the public bash.ws test, and flags resolvers outside your VPN.
- **VPN drop alerts** (free): background check, desktop notification when the public IP falls back to the home IP.
- 100 % free since 1.0.2: no account, no paid tier. When a leak is found, the popup links to the vpnsmith.com VPN comparison (affiliate links, disclosed).

Built by the team behind [vpnsmith.com](https://www.vpnsmith.com?src=github&ref=gh-vpn-leak-guard). No analytics, no servers. See [PRIVACY.md](PRIVACY.md).

## Load it unpacked

1. `chrome://extensions`, enable Developer mode.
2. "Load unpacked", pick this folder.

## Package for the Chrome Web Store

```bash
python3 tools/pack.py   # writes dist/vpn-leak-guard-<version>.zip
```

## Layout

- `manifest.json` (MV3), `popup.html|css|js`, `background.js` (service worker), `config.js` (every outbound link).
- `store/`: listing copy and permission justifications.
