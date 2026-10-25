#!/usr/bin/env python3
"""Zip the extension for Firefox AMO: same code, manifest adapted (background.scripts, gecko id)."""
import json, zipfile, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
m = json.load(open(root / "manifest.json"))
m["background"] = {"scripts": ["config.js", "vendor/ExtPay.js", "background.js"]}
m.pop("minimum_chrome_version", None)
m["browser_specific_settings"] = {"gecko": {
    "id": "vpn-leak-guard@vpnsmith.com", "strict_min_version": "128.0",
    "data_collection_permissions": {"required": ["none"]}}}
dist = root / "dist"; dist.mkdir(exist_ok=True)
out = dist / f"vpn-leak-guard-firefox-{m['version']}.zip"
skip_dirs = {".git", "dist", "store", "tools", "node_modules"}
skip_files = {"README.md", "PRIVACY.md", ".gitignore", "icon-1024.png", "manifest.json", "background.js"}
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("manifest.json", json.dumps(m, indent=2))
    bg = (root / "background.js").read_text().replace('importScripts("config.js", "vendor/ExtPay.js");', "")
    z.writestr("background.js", bg)
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if p.is_dir() or rel.parts[0] in skip_dirs or p.name in skip_files:
            continue
        z.write(p, str(rel))
print(out, out.stat().st_size, "bytes")
