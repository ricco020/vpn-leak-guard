// Single place for every outbound link and identifier.
// Affiliate links go through vpnsmith.com/go/<slug> (302 + server-side click log),
// never to the partner directly, so attribution stays measurable per source.
const VLG = {
  // 1.0.2: 100 % free, no payment code at all. Revenue comes only from the
  // disclosed affiliate links below, shown when a leak is detected.
  SRC: "ext-leak-guard",
  IP_API: "https://ipwho.is/",
  IP_API_FALLBACK: "https://api.ipify.org?format=json",
  // DNS leak test: bash.ws (public service, CORS open). The browser resolves a few
  // random subdomains of a fresh test id, then bash.ws lists the resolvers it saw.
  DNS_API: "https://bash.ws",
  STUN: [
    { urls: "stun:stun.l.google.com:19302" },
    { urls: "stun:stun.cloudflare.com:3478" }
  ],
  WATCH_MINUTES_DEFAULT: 2,
  links: {
    fullTest:
      "https://www.vpnsmith.com/en/tools/ip-leak-test?utm_source=chrome-extension&utm_medium=extension&utm_campaign=vpn-leak-guard",
    wireguard:
      "https://www.vpnsmith.com/en/tools/wireguard-config-generator?utm_source=chrome-extension&utm_medium=extension&utm_campaign=vpn-leak-guard",
    compare:
      "https://www.vpnsmith.com/en/blog/self-hosted-vpn-vs-paid-vpn-2026?utm_source=chrome-extension&utm_medium=extension&utm_campaign=vpn-leak-guard&utm_content=leak-compare",
    nordvpn: "https://www.vpnsmith.com/go/nordvpn?src=ext-leak-guard&pos=leak",
    contabo: "https://www.vpnsmith.com/go/contabo-vps-2y?src=ext-leak-guard&pos=selfhost",
    site: "https://www.vpnsmith.com/?utm_source=chrome-extension&utm_medium=extension&utm_campaign=vpn-leak-guard",
    privacy: "https://github.com/ricco020/vpn-leak-guard/blob/main/PRIVACY.md"
  }
};
if (typeof globalThis !== "undefined") globalThis.VLG = VLG;
