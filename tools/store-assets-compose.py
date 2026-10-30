# Compose the 1280x800 store screenshots from the popup shots of store-assets-capture.py (1.0.3).
# Store rules: the real popup fills most of the frame, a short benefit as title, plain flat background (no grid, no band).
import base64, os
from playwright.sync_api import sync_playwright
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts"); ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "icons", "icon-128.png"); OUT = "/mnt/c/Users/lerer/Desktop/Affil/VpnLeakGuard/store/assets"; os.makedirs(OUT, exist_ok=True)
def b64(p): return base64.b64encode(open(p, "rb").read()).decode()
fonts = f"""
@font-face {{ font-family:"Space Grotesk"; src:url(data:font/woff2;base64,{b64(F+'/space-grotesk-700.woff2')}) format("woff2"); font-weight:700; }}
@font-face {{ font-family:"Plex Sans"; src:url(data:font/woff2;base64,{b64(F+'/plex-sans-var.woff2')}) format("woff2"); font-weight:100 700; }}
@font-face {{ font-family:"Plex Mono"; src:url(data:font/woff2;base64,{b64(F+'/plex-mono-600.woff2')}) format("woff2"); font-weight:600; }}
"""
CSS = fonts + """
html,body{margin:0;width:1280px;height:800px;overflow:hidden;background:#0d1219;color:#e8ecf2;font-family:"Plex Sans",sans-serif}
.left{position:absolute;left:96px;top:0;height:800px;width:560px;display:flex;flex-direction:column;justify-content:center}
.k{font-family:"Plex Mono",monospace;font-size:15px;letter-spacing:.2em;color:ACC;font-weight:600;margin-bottom:20px}
h1{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:64px;line-height:1.02;letter-spacing:-.02em;margin:0 0 24px}
p{font-size:22px;line-height:1.5;color:#b3bcc8;margin:0;max-width:500px}
.shot{position:absolute;right:96px;top:50%;transform:translateY(-50%);width:__SW__;overflow:hidden;border-radius:16px;box-shadow:0 30px 70px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.10)}
.shot img{width:__SW__;display:block}
.brand{position:absolute;left:96px;top:56px;display:flex;align-items:center;gap:16px;font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:28px;letter-spacing:-.01em}
.brand img{width:56px;height:56px}
.pair{position:absolute;right:72px;top:50%;transform:translateY(-50%);display:flex;gap:28px;align-items:flex-start}
.pair .shot{position:static;transform:none;width:330px}.pair .shot img{width:330px}
.tag{font-family:"Plex Mono",monospace;font-weight:600;font-size:15px;letter-spacing:.2em;margin:0 0 12px 4px}
.chips{display:flex;gap:10px;margin-top:28px;flex-wrap:wrap}.chips span{font-family:"Plex Mono",monospace;font-weight:600;font-size:15px;letter-spacing:.06em;padding:8px 12px;border:1px solid rgba(255,255,255,.22);border-radius:6px;color:#e8ecf2}
.wide .left{width:480px}
.narrow .left{width:400px}.narrow h1{font-size:54px}.narrow p{font-size:20px;max-width:380px}
"""
LIME, ORANGE = "#c8ff3c", "#ff6a3d"
FRAMES = [
 ("01-leak-test", "leak-top", ORANGE, "WEBRTC LEAK TEST", "See what your VPN leaks",
  "Public IP, WebRTC, DNS resolvers and timezone, checked in one click. The answer comes first."),
 ("02-dns-leak", "dns", ORANGE, "DNS LEAK TEST", "Catch DNS leaks too",
  "The browser resolves test names and the extension lists which resolvers answered. A resolver outside your VPN is flagged."),
 ("03-blocked", ("leak", "blocked"), LIME, "ONE-CLICK FIX", "Leak found, then fixed",
  "One switch turns on Chrome's own WebRTC policy and the next test comes back clean. No server, no account."),
 ("04-no-leak", "recap", LIME, "IP · WEBRTC · DNS STATUS", "Every check, one status",
  "Public IP, WebRTC, DNS and timezone each get a plain status. Save your home IP once and the test knows what must never show. Free, including drop alerts."),
]
def html(f):
    key, shot, acc, k, h, p = f
    css = CSS.replace('__SW__', '520px' if shot in ('recap', 'leak-top') else '430px')
    chips = '<div class="chips"><span>FREE</span><span>NO ACCOUNT</span><span>ONE-CLICK WEBRTC BLOCK</span></div>' if key.startswith('01') else ''
    img = lambda n: f'<div class="shot"><img src="data:image/png;base64,{b64("/tmp/cws/shots/"+n+".png")}"></div>'
    if isinstance(shot, tuple):
        right = (f'<div class="pair"><div><div class="tag" style="color:{ORANGE}">BEFORE</div>{img(shot[0])}</div>'
                 f'<div><div class="tag" style="color:{LIME}">AFTER</div>{img(shot[1])}</div></div>')
        cls = "narrow"
    else:
        right, cls = img(shot), ("wide" if shot in ('recap', 'leak-top') else "")
    return f"""<!doctype html><html><head><style>{css.replace('ACC', acc)}</style></head><body class="{cls}">
<div class="brand"><img src="data:image/png;base64,{b64(ICON)}">VPN Leak Guard</div>
<div class="left"><div class="k">{k}</div><h1>{h}</h1><p>{p}</p>{chips}</div>
{right}</body></html>"""
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 800})
    for f in FRAMES:
        pg.set_content(html(f)); pg.wait_for_timeout(600)
        pg.screenshot(path=f"{OUT}/screenshot-{f[0]}.png"); print("ok", f[0])
    b.close()
