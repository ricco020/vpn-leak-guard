# Chrome Web Store listing: VPN Leak Guard

## Name (45 max)
VPN Leak Guard: WebRTC, DNS & IP Leak Test

## Summary (132 max)
Free WebRTC leak test, DNS leak test and IP check in one click, plus WebRTC leak blocking and VPN drop alerts. No account.

## Category
Privacy & Security (Productivity > Privacy)

## Description
Is your VPN really hiding your IP? Run a WebRTC leak test and a DNS leak test in one click, from your toolbar, in a few seconds. Most VPN apps protect your traffic but not WebRTC, a browser feature that can hand your real address to any website, and many leave DNS requests going to your provider. VPN Leak Guard is 100 % free: no account, no paid tier, no ads.

WHAT IT CHECKS
- Public IP: the address every website sees, with ISP and location.
- WebRTC: the addresses your browser exposes through STUN. If one differs from your public IP, that is a leak, and the guard says so plainly.
- DNS leak test: your browser resolves a few random names of a fresh test id, and the public bash.ws service reports which DNS resolvers asked for them. If they sit outside your VPN, your provider can log every site you open: that is a DNS leak.
- Timezone: whether your browser timezone matches your IP's. A mismatch is what fingerprinting scripts use to flag VPN users.

WHAT IT FIXES
- Block WebRTC leaks with one toggle. The extension sets Chrome's WebRTC policy to the proxied route only. Video calls keep working on most services. Turn it off any time.
- Home IP: save your real IP once (while the VPN is off). From then on the guard can prove your VPN hides it, instead of guessing.

VPN DROP ALERTS (FREE)
VPNs disconnect silently. Turn on "Watch my VPN" and the guard checks your public IP in the background every 2 minutes, then shows a desktop notification the moment it falls back to your home IP, with a red badge on the icon.

PRIVACY
No analytics, no servers, no browsing data. The only network requests are the IP lookup (ipwho.is, api.ipify.org), STUN, and the DNS leak test (bash.ws). Settings and results stay in Chrome's local storage. Full policy: https://github.com/ricco020/vpn-leak-guard/blob/main/PRIVACY.md

Built by the team behind vpnsmith.com, where you will find the full leak test, a free WireGuard config generator and our VPN reviews. When a leak is found, the popup links to our VPN comparison and to one VPN provider; these contain affiliate links and we may earn a commission. The extension itself costs nothing.

## Permission justifications (Developer Dashboard)
- privacy: to read and, on the user's explicit toggle, set `chrome.privacy.network.webRTCIPHandlingPolicy` (the WebRTC leak blocker).
- storage: to keep the user's saved home IP, last test result and settings locally.
- alarms: free background VPN drop check at a user-chosen interval (default 2 minutes).
- notifications: free desktop alert when the public IP matches the saved home IP.
- host permissions https://ipwho.is/* and https://api.ipify.org/*: fetching the user's public IP, ISP and timezone, which is the whole point of the leak comparison. The DNS leak test calls bash.ws, which allows any origin (CORS), so it needs no host permission.
- Remote code: none. Single purpose: test and block IP leaks around a VPN.

## Pricing
Free since 1.0.2 (29/10/2026, benchmark: the leader WebRTC Leak Prevent, ~90 k users, is free and no paid competitor sells). Revenue = affiliate clicks on a detected leak (utm_content=leak-compare, sid ext-leak-guard).

## Assets
- Icon 128: icons/icon-128.png (generated 17/10/2026, image.py, 0.053 USD).
- Screenshots 1280x800 (4), redone 30/10/2026 08:00 for the 1.0.4 popup (upload at the next console session, in this order): screenshot-01-leak-test.png (WebRTC leak, answer only, chips Free / No account / One-click WebRTC block), screenshot-02-dns-leak.png (DNS leak), screenshot-03-blocked.png (before/after: leak then WebRTC blocking on, verdict 'No leak found by these tests'), screenshot-04-no-leak.png (status recap: public IP, WebRTC, DNS, timezone). Plain flat background, no grid, no side band. Real popup, mocked network answers, documentation IPs only (203.0.113.42 VPN, 198.51.100.7 home, 203.0.113.53 / 198.51.100.53 resolvers). Remove the old 02-fix and 04-pro (Pro 4.99 USD no longer exists). Rebuild: copy the extension to /tmp/vlg-ext, xvfb-run -a python3 tools/store-assets-capture.py, then python3 tools/store-assets-compose.py. Design judge 5.5 -> 5.8.
- Small promo tile 440x280: store/assets/promo-tile-440x280.png.
- Chrome Web Store publisher: d2668f16-53c2-4f15-b0cb-b06a63206b45 (registered 18/10/2026, display name VPNSmith). ExtensionPay: registered 18/10/2026 but removed from the extension in 1.0.2 (100 % free).

## Cross-links to our sites (all tracked)
- /go/nordvpn?src=ext-leak-guard&pos=leak (CJ, sid = ext-leak-guard)
- /go/contabo-vps-2y?src=ext-leak-guard&pos=selfhost (CJ, sid = ext-leak-guard)
- 1.0.4 : premiere installation = 1 onglet /en/tools/ip-leak-test utm_content=welcome (jamais a la mise a jour) ; desinstallation = /en/blog/self-hosted-vpn-vs-paid-vpn-2026 utm_content=uninstall (URL fixe, aucune donnee). Aucune permission ajoutee (tabs.create et setUninstallURL n'en demandent pas).
- Tools on vpnsmith.com with utm_source=chrome-extension
