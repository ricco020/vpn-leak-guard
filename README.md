# VPN Leak Guard: WebRTC & IP Leak Test (Chrome extension)

One click tells you whether your VPN really hides your IP:

- **Public IP** as websites see it (ISP, location).
- **WebRTC** candidates gathered through STUN, compared with the public IP: a mismatch is a leak.
- **Timezone** consistency between the browser and the IP.
- **Block WebRTC leaks** toggle (sets Chrome's `webRTCIPHandlingPolicy` to `disable_non_proxied_udp`).
- **Home IP**: save your real IP once, and the guard can prove the VPN hides it.
- **Pro**: background VPN drop alerts (desktop notification when the public IP falls back to the home IP). Payment through ExtensionPay.

Built by the team behind [vpnsmith.com](https://www.vpnsmith.com). No analytics, no servers. See [PRIVACY.md](PRIVACY.md).

## Load it unpacked

1. `chrome://extensions`, enable Developer mode.
2. "Load unpacked", pick this folder.

## Package for the Chrome Web Store

```bash
python3 tools/pack.py   # writes dist/vpn-leak-guard-<version>.zip
```

## Layout

- `manifest.json` (MV3), `popup.html|css|js`, `background.js` (service worker), `config.js` (every outbound link).
- `vendor/ExtPay.js`: ExtensionPay client (MIT), extension id `vpn-leak-guard`.
- `store/`: listing copy and permission justifications.
