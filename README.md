# VPN Leak Guard: WebRTC & IP Leak Test (Chrome extension)

**[Install from the Chrome Web Store](https://chromewebstore.google.com/detail/dlpikagegmmcphbaalmcedldgpnononn?utm_source=github&utm_medium=readme&utm_campaign=vpn-leak-guard)** (free, version 1.0.8, store listing in 19 languages, interface in English).

Prefer to test without installing anything? Run the same IP, WebRTC and DNS checks in the page: [IP, WebRTC and DNS leak test on vpnsmith.com](https://www.vpnsmith.com/en/tools/ip-leak-test?src=github&ref=gh-vpn-leak-guard).

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

## Why the popup sends you to a web page to confirm the WebRTC fix

Measured while building the extension (Chromium, Manifest V3, October 2026): after
`chrome.privacy.network.webRTCIPHandlingPolicy` is set to `disable_non_proxied_udp`, an ordinary
site such as `example.com` gathers no WebRTC candidate, but the extension's own popup still gathers
both the host and the server-reflexive (srflx) candidates. Chrome does not apply that policy to
extension pages. A popup that tested itself would keep reporting a leak that websites can no
longer see, so the popup labels the state "blocked on sites" and links to a real web page for the
proof. If you build a WebRTC blocker, test the policy from a normal tab, never from
`chrome-extension://` pages.

## Other browsers

Chrome and Chromium-based browsers only for now. In Firefox you can turn WebRTC off without an
extension (`media.peerconnection.enabled` = `false` in `about:config`), then confirm with the
[leak test](https://www.vpnsmith.com/en/tools/ip-leak-test?src=github&ref=gh-vpn-leak-guard).
