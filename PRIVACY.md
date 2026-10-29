# VPN Leak Guard: Privacy Policy

Last updated: 2026-10-17

VPN Leak Guard is a Chrome extension published by Eric Gerard (vpnsmith.com).

## What the extension does with data

- **Public IP lookup.** When you open the popup or run a test, the extension asks `https://ipwho.is/` (fallback `https://api.ipify.org`) for your public IP address, ISP and timezone. That request necessarily sends your IP to that service, exactly as visiting any website does. We do not receive or store it on our servers; we have no servers.
- **WebRTC test.** The extension opens a local RTCPeerConnection to public STUN servers (Google, Cloudflare) to see which addresses WebRTC would expose. Results are shown to you and never sent anywhere.
- **Local storage only.** Your saved home IP, the last test result and your settings are stored in Chrome's local extension storage on your device. They are never uploaded.
- **Chrome WebRTC policy.** With your consent (the toggle), the extension changes Chrome's `webRTCIPHandlingPolicy` setting. You can revert it at any time from the popup.
- **DNS leak test.** Each test asks `https://bash.ws/` (a public DNS leak test service) for a random test id, makes your browser look up a few random subdomains of `bash.ws`, then reads back the list of DNS resolvers that performed those lookups. bash.ws therefore sees your public IP and your resolvers' IPs, as any website would. Nothing else is sent.
- **No payments.** Since version 1.0.2 the extension is entirely free and contains no payment code.
- **Notifications.** The Pro "VPN drop alerts" feature checks your public IP in the background at the interval you chose and shows a desktop notification when it matches your saved home IP. Nothing leaves your device except that IP lookup.

## What we do not do

- No analytics, no tracking pixels, no fingerprinting.
- No browsing history access: the extension does not read page content and has no content scripts at all.
- No selling or sharing of data.

## Affiliate links

Links in the popup to vpnsmith.com, NordVPN and Contabo are affiliate links: if you buy through them we may earn a commission at no cost to you. Clicking is always your choice.

## Contact

Questions: open an issue on https://github.com/ricco020/vpn-leak-guard
