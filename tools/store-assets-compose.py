import base64, time, os
from playwright.sync_api import sync_playwright
F="/tmp/vlg-ext/fonts"; OUT="/mnt/c/Users/lerer/Desktop/Affil/VpnLeakGuard/store/assets"; os.makedirs(OUT, exist_ok=True)
def b64(p): return base64.b64encode(open(p,"rb").read()).decode()
fonts = f"""
@font-face {{ font-family:"Space Grotesk"; src:url(data:font/woff2;base64,{b64(F+'/space-grotesk-700.woff2')}) format("woff2"); font-weight:700; }}
@font-face {{ font-family:"Plex Mono"; src:url(data:font/woff2;base64,{b64(F+'/plex-mono-400.woff2')}) format("woff2"); font-weight:400; }}
@font-face {{ font-family:"Plex Mono"; src:url(data:font/woff2;base64,{b64(F+'/plex-mono-600.woff2')}) format("woff2"); font-weight:600; }}
"""
NOISE="url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.5'/%3E%3C/svg%3E\")"
CSS = fonts + """
html,body{margin:0;width:1280px;height:800px;overflow:hidden;background:#0b0f16;color:#e8ecf2;font-family:"Plex Mono",monospace}
.bg{position:absolute;inset:0;background:
 radial-gradient(900px 600px at 85% 20%, rgba(200,255,60,.10), transparent 60%),
 radial-gradient(700px 500px at 10% 90%, rgba(255,106,61,.12), transparent 60%),
 linear-gradient(160deg,#0f1520 0%,#0b0f16 60%,#090c12 100%)}
.bg:after{content:"";position:absolute;inset:0;background-image:NOISE;opacity:.18;mix-blend-mode:overlay}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:64px 64px}
.left{position:absolute;left:84px;top:0;height:800px;width:560px;display:flex;flex-direction:column;justify-content:center}
.k{font-size:15px;letter-spacing:.22em;color:#c8ff3c;font-weight:600;margin-bottom:22px}
.k.bad{color:#ff6a3d}
h1{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:58px;line-height:1.02;letter-spacing:-.02em;margin:0 0 26px}
p{font-size:21px;line-height:1.5;color:#aab3c0;margin:0 0 22px;max-width:520px}
.badge{display:inline-block;border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:8px 16px;font-size:14px;letter-spacing:.08em;color:#e8ecf2}
.shot{position:absolute;right:120px;top:TOP;width:380px;height:HEIGHT;overflow:hidden;border-radius:18px;box-shadow:0 40px 90px rgba(0,0,0,.65),0 0 0 1px rgba(255,255,255,.08)}
.shot img{width:380px;display:block;position:relative;top:OFF}
.shot:after{content:"";position:absolute;left:0;right:0;bottom:0;height:90px;background:linear-gradient(transparent,#0b0f16)}
.notif{position:absolute;right:60px;top:560px;width:420px;background:#1c2027;border-radius:12px;padding:16px 18px 16px 64px;box-shadow:0 24px 60px rgba(0,0,0,.6);font-family:system-ui,sans-serif;color:#e8ecf2;transform:rotate(-2deg)}
.notif img{position:absolute;left:16px;top:16px;width:34px;height:34px;border-radius:8px}
.notif b{display:block;font-size:15px;margin-bottom:4px}.notif span{font-size:13px;color:#b7bec9;line-height:1.35}.notif i{position:absolute;right:14px;top:12px;font-style:normal;font-size:11px;color:#8b93a1}
""".replace("NOISE", NOISE)
ICON = b64("/tmp/vlg-ext/icons/icon-128.png")
FRAMES = [
 ("01-leak-test", "leak", "0px|40px|760px", "LEAK TEST", "bad", "Is your VPN really hiding your IP?",
  "One click shows the IP every website sees, what WebRTC exposes, and whether your timezone gives you away.", "Public IP · WebRTC · Timezone", False),
 ("02-fix", "leak", "-400px|80px|640px", "FIX IT", "", "Leak found? Fix it with one toggle.",
  "Block WebRTC leaks with Chrome's own policy, or pick a VPN that blocks them. Your saved home IP tells the guard what must never show.", "Chrome policy · no server · no account", False),
 ("03-blocked", "blocked", "0px|40px|760px", "PROTECTED", "", "WebRTC blocked on every website",
  "Chrome routes WebRTC through your VPN only. Video calls keep working on most services, and you can turn it off any time.", "Verdict in a few seconds", False),
 ("04-pro", "pro", "-262px|60px|500px", "PRO · VPN DROP ALERTS", "", "Know the second your VPN drops",
  "Pro checks your public IP every 2 minutes in the background and shows a desktop notification when your home IP comes back.", "One payment · 4.99 USD · Stripe", True),
]
def html(f):
    key, shot, off, k, kc, h, p, badge, notif = f
    off, top, height = off.split("|")
    n = f"""<div class="notif"><img src="data:image/png;base64,{ICON}"><i>Google Chrome</i><b>VPN Leak Guard: your real IP is visible</b><span>Your public IP (198.51.100.7) is the home IP you saved. Your VPN looks disconnected.</span></div>""" if notif else ""
    return f"""<!doctype html><html><head><style>{CSS.replace('OFF', off).replace('TOP', top).replace('HEIGHT', height)}</style></head><body>
<div class="bg"></div><div class="grid"></div>
<div class="left"><div class="k {kc}">{k}</div><h1>{h}</h1><p>{p}</p><div><span class="badge">{badge}</span></div></div>
<div class="shot"><img src="data:image/png;base64,{b64('/tmp/cws/shots/'+shot+'.png')}"></div>{n}</body></html>"""
TILE = f"""<!doctype html><html><head><style>{fonts}
html,body{{margin:0;width:440px;height:280px;overflow:hidden;background:#0b0f16;color:#e8ecf2;font-family:"Plex Mono",monospace}}
.bg{{position:absolute;inset:0;background:radial-gradient(400px 260px at 90% 10%, rgba(200,255,60,.14), transparent 60%),radial-gradient(300px 220px at 5% 100%, rgba(255,106,61,.14), transparent 60%),linear-gradient(160deg,#0f1520,#090c12)}}
.bg:after{{content:"";position:absolute;inset:0;background-image:{NOISE};opacity:.2;mix-blend-mode:overlay}}
.w{{position:absolute;left:32px;top:0;height:280px;display:flex;align-items:center;gap:24px}}
img{{width:96px;height:96px;border-radius:22px;box-shadow:0 18px 40px rgba(0,0,0,.6)}}
h1{{font-family:"Space Grotesk",sans-serif;font-size:34px;line-height:1;margin:0 0 10px;letter-spacing:-.02em}}
p{{margin:0;font-size:14px;color:#aab3c0;line-height:1.45;max-width:250px}}
.k{{font-size:11px;letter-spacing:.22em;color:#c8ff3c;font-weight:600;margin-bottom:8px}}
</style></head><body><div class="bg"></div><div class="w"><img src="data:image/png;base64,{ICON}"><div><div class="k">CHROME EXTENSION</div><h1>VPN Leak Guard</h1><p>WebRTC & IP leak test, one-toggle blocking, VPN drop alerts.</p></div></div></body></html>"""
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width":1280,"height":800})
    for f in FRAMES:
        pg.set_content(html(f)); pg.wait_for_timeout(600)
        pg.screenshot(path=f"{OUT}/screenshot-{f[0]}.png"); print("ok", f[0])
    pg2 = b.new_page(viewport={"width":440,"height":280}); pg2.set_content(TILE); pg2.wait_for_timeout(600)
    pg2.screenshot(path=f"{OUT}/promo-tile-440x280.png"); print("ok tile")
    b.close()
