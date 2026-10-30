# Store screenshots of the 1.0.3 popup, from the real extension with mocked network answers.
# Documentation IPs only (RFC 5737): 203.0.113.42 = VPN exit, 198.51.100.7 = saved home IP.
# Scenarios: protected (no leak found), leak (WebRTC shows home IP), blocked (WebRTC blocking on), dns (resolvers leak).
# Usage: copy the extension to /tmp/vlg-ext, then xvfb-run -a python3 tools/store-assets-capture.py
import sys, json, os
from playwright.sync_api import sync_playwright
EXT = "/tmp/vlg-ext"; PROF = "/tmp/vlg-shot-profile"; OUT = "/tmp/cws/shots"
os.system(f"rm -rf {PROF}"); os.makedirs(OUT, exist_ok=True)
VPN_IP = "203.0.113.42"; HOME_IP = "198.51.100.7"
MOCK = {"ip": VPN_IP, "success": True, "country": "Netherlands", "country_code": "NL", "city": "Amsterdam",
        "connection": {"isp": "Example VPN B.V.", "org": "Example VPN B.V."}, "timezone": {"id": "Europe/Amsterdam"}}
DNS_OK = [{"ip": "203.0.113.53", "country_name": "Netherlands", "country": "nl", "asn": "Example VPN B.V.", "type": "dns"},
          {"ip": "Your IP is not leaking", "type": "conclusion"}]
DNS_LEAK = [{"ip": "203.0.113.53", "country_name": "Netherlands", "country": "nl", "asn": "Example VPN B.V.", "type": "dns"},
            {"ip": "198.51.100.53", "country_name": "France", "country": "fr", "asn": "Example Home ISP", "type": "dns"},
            {"ip": "DNS may be leaking.", "type": "conclusion"}]
INIT = """
(() => {
  const scn = (location.hash || "").replace("#scn=", "") || "protected";
  const cands = {
    protected: [["203.0.113.42","srflx"],["192.168.1.24","host"]],
    leak:      [["198.51.100.7","srflx"],["192.168.1.24","host"]],
    blocked:   [["203.0.113.42","srflx"]],
    dns:       [["203.0.113.42","srflx"],["192.168.1.24","host"]],
  }[scn] || [];
  class FakePC {
    constructor(){ this.onicecandidate=null; }
    createDataChannel(){ return {}; }
    createOffer(){ return Promise.resolve({type:"offer",sdp:""}); }
    setLocalDescription(){
      setTimeout(()=>{ for (const [ip,typ] of cands) this.onicecandidate && this.onicecandidate({candidate:{candidate:`candidate:1 1 udp 2113937151 ${ip} 54321 typ ${typ} generation 0`}});
        this.onicecandidate && this.onicecandidate({candidate:null}); }, 300);
      return Promise.resolve(); }
    close(){}
  }
  window.RTCPeerConnection = FakePC;
})();
"""
SCN = {"cur": "protected"}
def dns_route(r):
    u = r.request.url
    if u.endswith("/id"): return r.fulfill(status=200, content_type="text/plain", body="a1b2c3d4e5f6")
    if "/dnsleak/test/" in u:
        return r.fulfill(status=200, content_type="application/json", body=json.dumps(DNS_LEAK if SCN["cur"] == "dns" else DNS_OK))
    return r.abort()
def run(scn, ctx, ext_id):
    SCN["cur"] = scn
    p = ctx.new_page()
    p.goto(f"chrome-extension://{ext_id}/popup.html#scn={scn}")
    p.wait_for_timeout(1500)
    if scn == "blocked":
        p.evaluate("() => chrome.storage.local.remove(['homeIp','homeSetAt'])")
        p.evaluate("() => chrome.privacy.network.webRTCIPHandlingPolicy.set({value:'disable_non_proxied_udp'})")
    else:
        p.evaluate("([h]) => chrome.storage.local.set({homeIp:h, homeSetAt: Date.now()})", [HOME_IP])
        p.evaluate("() => chrome.privacy.network.webRTCIPHandlingPolicy.set({value:'default'})")
    p.reload(); p.wait_for_timeout(9000)
    print(scn, "|", p.inner_text("#verdict").replace("\n", " / ")[:200])
    # crop to the popup content (the body is shorter than the frame)
    h = p.evaluate("() => Math.ceil(Math.max(...[...document.body.children].map(e => e.getBoundingClientRect().bottom)) + 14)")
    p.screenshot(path=f"{OUT}/{scn}.png", clip={"x": 0, "y": 0, "width": 380, "height": min(h, 640)})
    p.close()
with sync_playwright() as pw:
    ctx = pw.chromium.launch_persistent_context(PROF, headless=False, viewport={"width": 380, "height": 640}, device_scale_factor=2,
        timezone_id="Europe/Amsterdam", locale="en-US",
        args=[f"--disable-extensions-except={EXT}", f"--load-extension={EXT}", "--lang=en-US"])
    ctx.route("https://ipwho.is/**", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK)))
    ctx.route("https://api.ipify.org**", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps({"ip": VPN_IP})))
    ctx.route("**/*bash.ws/**", dns_route)
    ctx.add_init_script(INIT)
    sw = ctx.service_workers
    if not sw: sw = [ctx.wait_for_event("serviceworker", timeout=20000)]
    ext_id = sw[0].url.split("/")[2]; print("ext id", ext_id)
    for scn in (sys.argv[1:] or ["protected", "leak", "blocked", "dns"]):
        run(scn, ctx, ext_id)
    ctx.close()
