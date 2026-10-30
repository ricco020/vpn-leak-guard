#!/usr/bin/env python3
"""Relais Chrome Web Store : envoie et publie la version suivante des que l'examen en cours est fini.

Pourquoi : un nouvel envoi remplace le paquet en examen, donc la version suivante attend que la fiche
publique serve la version soumise. Sans relais, ce delai depend du passage d'un ouvrier (heures).
Lance par cron toutes les 20 min ; idempotent (marqueur d'etat), silencieux quand rien ne change.

Regle : fiche servie == crxVersion du brouillon (examen termine) ET brouillon < CIBLE
        -> PUT upload CIBLE, verifie uploadState SUCCESS + crxVersion == CIBLE, puis publish.
Usage : python3 cws-relais.py [--dry]
"""
import json, os, re, subprocess, sys, time, urllib.request

ITEM = "dlpikagegmmcphbaalmcedldgpnononn"
CIBLE = "1.0.4"
ICI = os.path.dirname(os.path.abspath(__file__))
ZIP = os.path.join(ICI, "..", "dist", f"vpn-leak-guard-{CIBLE}.zip")
LOG = "/mnt/c/Users/lerer/Desktop/Orch/state/cws-relais.log"
FAIT = os.path.expanduser(f"~/.config/factories/cws-relais-{ITEM}-{CIBLE}.done")
sys.path.insert(0, "/mnt/c/Users/lerer/Desktop/Orch/outils")
import cws  # noqa: E402

v = lambda s: tuple(int(x) for x in s.split("."))


def journal(msg):
    with open(LOG, "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M ") + msg + "\n")
    print(msg)


def servie():
    req = urllib.request.Request(f"https://chromewebstore.google.com/detail/{ITEM}?hl=en",
                                 headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    m = re.search(r"Version</div><div[^>]*>([0-9.]+)<", html)
    return m.group(1) if m else None


def main():
    dry = "--dry" in sys.argv
    if os.path.exists(FAIT):
        return
    s = servie()
    st = cws.appel("GET", f"{cws.API}/chromewebstore/v1.1/items/{ITEM}?projection=DRAFT")
    brouillon = st.get("crxVersion")
    if not s or not brouillon:
        journal(f"lecture impossible : servie={s} brouillon={brouillon} {str(st)[:200]}")
        return
    if v(s) >= v(CIBLE):
        open(FAIT, "w").write(s)
        journal(f"{CIBLE} servie, relais termine")
        return
    if v(brouillon) >= v(CIBLE):
        if dry:
            print(f"servie {s}, {CIBLE} deja en examen")
        return
    if s != brouillon:
        if dry:
            print(f"servie {s}, brouillon {brouillon} encore en examen : rien")
        return
    if not os.path.exists(ZIP):
        subprocess.run([sys.executable, os.path.join(ICI, "pack.py")], check=True, timeout=300)
    journal(f"examen de {brouillon} termine (servie {s}) : envoi {CIBLE}" + (" [dry]" if dry else ""))
    if dry:
        return
    up = cws.appel("PUT", f"{cws.API}/upload/chromewebstore/v1.1/items/{ITEM}", open(ZIP, "rb").read(),
                   {"Content-Type": "application/zip"})
    if up.get("uploadState") != "SUCCESS" or up.get("crxVersion") != CIBLE:
        journal(f"envoi refuse : {json.dumps(up)[:400]}")
        return
    pub = cws.appel("POST", f"{cws.API}/chromewebstore/v1.1/items/{ITEM}/publish", b"", {"Content-Length": "0"})
    journal(f"publication {CIBLE} : {json.dumps(pub)[:300]}")


if __name__ == "__main__":
    main()
