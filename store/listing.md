# Chrome Web Store listing: VPN Leak Guard

## Name (45 max)
VPN Leak Guard: WebRTC & IP Leak Test

## Summary (132 max)
One-click WebRTC and IP leak test, WebRTC leak blocking, and VPN drop alerts. Know if your VPN really hides your IP.

## Category
Privacy & Security (Productivity > Privacy)

## Description
Is your VPN really hiding your IP? Most VPN apps protect your traffic but not WebRTC, a browser feature that can hand your real address to any website in one call. VPN Leak Guard checks it in one click, from your toolbar, in a few seconds.

WHAT IT CHECKS
- Public IP: the address every website sees, with ISP and location.
- WebRTC: the addresses your browser exposes through STUN. If one differs from your public IP, that is a leak, and the guard says so plainly.
- Timezone: whether your browser timezone matches your IP's. A mismatch is what fingerprinting scripts use to flag VPN users.

WHAT IT FIXES
- Block WebRTC leaks with one toggle. The extension sets Chrome's WebRTC policy to the proxied route only. Video calls keep working on most services. Turn it off any time.
- Home IP: save your real IP once (while the VPN is off). From then on the guard can prove your VPN hides it, instead of guessing.

PRO: VPN DROP ALERTS
VPNs disconnect silently. Pro checks your public IP in the background every 2 minutes and shows a desktop notification the moment it falls back to your home IP, with a red badge on the icon. One payment through ExtensionPay (Stripe), no account to create.

PRIVACY
No analytics, no servers, no browsing data. The only network requests are the IP lookup (ipwho.is, api.ipify.org) and STUN. Settings and results stay in Chrome's local storage. Full policy: https://github.com/ricco020/vpn-leak-guard/blob/main/PRIVACY.md

Built by the team behind vpnsmith.com, where you will find the full leak test, a free WireGuard config generator and our VPN reviews. Some links in the popup are affiliate links.

## Permission justifications (Developer Dashboard)
- privacy: to read and, on the user's explicit toggle, set `chrome.privacy.network.webRTCIPHandlingPolicy` (the WebRTC leak blocker).
- storage: to keep the user's saved home IP, last test result and settings locally.
- alarms: Pro background VPN drop check at a user-chosen interval (default 2 minutes).
- notifications: Pro desktop alert when the public IP matches the saved home IP.
- host permissions https://ipwho.is/* and https://api.ipify.org/*: fetching the user's public IP, ISP and timezone, which is the whole point of the leak comparison. No other host is contacted.
- content script on https://extensionpay.com/*: ExtensionPay's payment confirmation callback (library requirement).
- Remote code: none. Single purpose: test and block IP leaks around a VPN.

## Pricing (to set in ExtensionPay)
Pro: 4.99 USD one-time (launch price). Alternative to test later: 1.99 USD/month.

## Assets
- Icon 128: icons/icon-128.png (generated 17/10/2026, image.py, 0.053 USD).
- Screenshots 1280x800 (4): store/assets/screenshot-01..04.png, made 18/10/2026 from the real popup with documentation IPs (203.0.113.42 as VPN, 198.51.100.7 as home, no real IP), composed with the extension's own fonts (tools: /tmp/cws/capture.py + compose.py, kept in tools/store-assets.py).
- Small promo tile 440x280: store/assets/promo-tile-440x280.png.
- Chrome Web Store publisher: d2668f16-53c2-4f15-b0cb-b06a63206b45 (registered 18/10/2026, display name VPNSmith). ExtensionPay: extension `vpn-leak-guard` registered 18/10/2026, plan `pro` 4.99 USD once; Stripe not connected yet.

## Cross-links to our sites (all tracked)
- /go/nordvpn?src=ext-leak-guard&pos=leak (CJ, sid = ext-leak-guard)
- /go/contabo-vps-2y?src=ext-leak-guard&pos=selfhost (CJ, sid = ext-leak-guard)
- Tools on vpnsmith.com with utm_source=chrome-extension
