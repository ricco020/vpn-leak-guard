// Single place for every outbound link and identifier.
// Affiliate links go through vpnsmith.com/go/<slug> (302 + server-side click log),
// never to the partner directly, so attribution stays measurable per source.
const VLG = {
  EXTPAY_ID: "vpn-leak-guard",
  SRC: "ext-leak-guard",
  IP_API: "https://ipwho.is/",
  IP_API_FALLBACK: "https://api.ipify.org?format=json",
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
    nordvpn: "https://www.vpnsmith.com/go/nordvpn?src=ext-leak-guard&pos=leak",
    contabo: "https://www.vpnsmith.com/go/contabo-vps-2y?src=ext-leak-guard&pos=selfhost",
    site: "https://www.vpnsmith.com/?utm_source=chrome-extension&utm_medium=extension&utm_campaign=vpn-leak-guard",
    privacy: "https://github.com/ricco020/vpn-leak-guard/blob/main/PRIVACY.md"
  }
};
if (typeof globalThis !== "undefined") globalThis.VLG = VLG;
