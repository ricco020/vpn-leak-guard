# Compose the 1280x800 store screenshots from the popup shots of store-assets-capture.py (1.0.3).
# Store rules: the real popup fills most of the frame, a 5-word benefit as title, flat brand background.
import base64, os
from playwright.sync_api import sync_playwright
F = "/tmp/vlg-ext/fonts"; OUT = "/mnt/c/Users/lerer/Desktop/Affil/VpnLeakGuard/store/assets"; os.makedirs(OUT, exist_ok=True)
def b64(p): return base64.b64encode(open(p, "rb").read()).decode()
fonts = f"""
@font-face {{ font-family:"Space Grotesk"; src:url(data:font/woff2;base64,{b64(F+'/space-grotesk-700.woff2')}) format("woff2"); font-weight:700; }}
@font-face {{ font-family:"Plex Sans"; src:url(data:font/woff2;base64,{b64(F+'/plex-sans-var.woff2')}) format("woff2"); font-weight:100 700; }}
@font-face {{ font-family:"Plex Mono"; src:url(data:font/woff2;base64,{b64(F+'/plex-mono-600.woff2')}) format("woff2"); font-weight:600; }}
"""
CSS = fonts + """
html,body{margin:0;width:1280px;height:800px;overflow:hidden;background:#0d1219;color:#e8ecf2;font-family:"Plex Sans",sans-serif}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:64px 64px}
.bar{position:absolute;left:0;top:0;bottom:0;width:10px;background:ACC}
.left{position:absolute;left:96px;top:0;height:800px;width:560px;display:flex;flex-direction:column;justify-content:center}
.k{font-family:"Plex Mono",monospace;font-size:15px;letter-spacing:.2em;color:ACC;font-weight:600;margin-bottom:20px}
h1{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:64px;line-height:1.02;letter-spacing:-.02em;margin:0 0 24px}
p{font-size:22px;line-height:1.5;color:#b3bcc8;margin:0;max-width:500px}
.shot{position:absolute;right:96px;top:50%;transform:translateY(-50%);width:__SW__;overflow:hidden;border-radius:16px;box-shadow:0 30px 70px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.10)}
.shot img{width:__SW__;display:block}
"""
LIME, ORANGE = "#c8ff3c", "#ff6a3d"
FRAMES = [
 ("01-leak-test", "leak", ORANGE, "WEBRTC LEAK TEST", "See what your VPN leaks",
  "Public IP, WebRTC, DNS resolvers and timezone, checked in one click. The answer comes first, the details stay folded."),
 ("02-dns-leak", "dns", ORANGE, "DNS LEAK TEST", "Catch DNS leaks too",
  "The browser resolves test names and the extension lists which resolvers answered. A resolver outside your VPN is flagged."),
 ("03-blocked", "blocked", LIME, "ONE-CLICK FIX", "Block WebRTC in one click",
  "Uses Chrome's own WebRTC policy: no server, no account. Turn it off any time from Settings."),
 ("04-no-leak", "protected", LIME, "CLEAR VERDICT", "A clear answer in seconds",
  "Save your home IP once and the test knows what must never show. Free, including drop alerts."),
]
def html(f):
    key, shot, acc, k, h, p = f
    css = CSS.replace('__SW__', '430px')
    return f"""<!doctype html><html><head><style>{css.replace('ACC', acc)}</style></head><body>
<div class="grid"></div><div class="bar"></div>
<div class="left"><div class="k">{k}</div><h1>{h}</h1><p>{p}</p></div>
<div class="shot"><img src="data:image/png;base64,{b64('/tmp/cws/shots/'+shot+'.png')}"></div></body></html>"""
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 800})
    for f in FRAMES:
        pg.set_content(html(f)); pg.wait_for_timeout(600)
        pg.screenshot(path=f"{OUT}/screenshot-{f[0]}.png"); print("ok", f[0])
    b.close()
