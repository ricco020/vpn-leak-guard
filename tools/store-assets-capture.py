import time, sys, json, os, re
from playwright.sync_api import sync_playwright
EXT="/tmp/vlg-ext"; PROF="/tmp/vlg-shot-profile"
os.system(f"rm -rf {PROF}")
VPN_IP="203.0.113.42"; HOME_IP="198.51.100.7"
MOCK={"ip":VPN_IP,"success":True,"country":"Netherlands","country_code":"NL","city":"Amsterdam",
      "connection":{"isp":"Example VPN B.V.","org":"Example VPN B.V."},"timezone":{"id":"Europe/Amsterdam"}}
INIT = """
(() => {
  const scn = (location.hash || "").replace("#scn=", "") || "protected";
  const cands = {
    protected: [["203.0.113.42","srflx"],["192.168.1.24","host"]],
    leak:      [["198.51.100.7","srflx"],["192.168.1.24","host"]],
    blocked:   [["203.0.113.42","srflx"]],
    pro:       [["203.0.113.42","srflx"],["192.168.1.24","host"]],
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
def run(scn, ctx, ext_id):
    p = ctx.new_page()
    p.goto(f"chrome-extension://{ext_id}/popup.html#scn={scn}")
    time.sleep(1.5)
    # storage + privacy state per scenario
    if scn in ("protected","leak","pro"):
        p.evaluate("""([h]) => chrome.storage.local.set({homeIp:h, homeSetAt: Date.now(), watchEnabled: true})""", [HOME_IP])
        p.evaluate("""() => chrome.privacy.network.webRTCIPHandlingPolicy.set({value:"default"})""")
    if scn == "blocked":
        p.evaluate("""() => chrome.storage.local.remove(["homeIp","homeSetAt"])""")
        p.evaluate("""() => chrome.privacy.network.webRTCIPHandlingPolicy.set({value:"disable_non_proxied_udp"})""")
    p.reload(); time.sleep(4.5)
    if scn == "pro":
        p.evaluate("""() => { const $=id=>document.getElementById(id);
          $("pro-badge").textContent="PRO ACTIVE"; $("pro-badge").classList.add("active");
          $("upgrade").classList.add("hidden"); $("watch-wrap").classList.remove("hidden"); $("watch-toggle").checked=true;
          $("pro-text").textContent="Background check every 2 minutes. You get a notification if your public IP falls back to your home IP."; }""")
        time.sleep(0.5)
    print(scn, "|", p.inner_text("#verdict").replace("\n"," / ")[:160], "| webrtc:", p.inner_text("#webrtc-state"), "| tz:", p.inner_text("#tz-state"), "| ip:", p.inner_text("#ip-state"))
    p.screenshot(path=f"/tmp/cws/shots/{scn}.png", full_page=True)
    p.close()
with sync_playwright() as pw:
    ctx = pw.chromium.launch_persistent_context(PROF, headless=False, viewport={"width":380,"height":700}, device_scale_factor=2,
        timezone_id="Europe/Amsterdam", locale="en-US",
        args=[f"--disable-extensions-except={EXT}", f"--load-extension={EXT}", "--lang=en-US"])
    ctx.route("https://ipwho.is/**", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK)))
    ctx.route("https://api.ipify.org**", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps({"ip":VPN_IP})))
    ctx.route("https://extensionpay.com/**", lambda r: r.abort())
    ctx.add_init_script(INIT)
    sw = ctx.service_workers
    if not sw: sw=[ctx.wait_for_event("serviceworker", timeout=20000)]
    ext_id = sw[0].url.split("/")[2]; print("ext id", ext_id)
    for scn in ["protected","leak","blocked","pro"]:
        run(scn, ctx, ext_id)
    ctx.close()
