// Popup logic. Everything runs locally; the only network calls are the two IP
// lookups declared in host_permissions (needed to know what websites see).
(function () {
  const $ = (id) => document.getElementById(id);
  const links = VLG.links;
  $("cta-nord").href = links.nordvpn;
  $("cta-compare").href = links.compare;
  $("link-full").href = links.fullTest;
  $("link-wg").href = links.wireguard;
  $("link-privacy").href = links.privacy;


  const PRIVATE_V4 = /^(10\.|127\.|192\.168\.|169\.254\.|172\.(1[6-9]|2\d|3[01])\.|0\.)/;
  const isIPv4 = (s) => /^\d{1,3}(\.\d{1,3}){3}$/.test(s);
  const isIPv6 = (s) => s.includes(":");
  const isPrivate = (ip) =>
    (isIPv4(ip) && PRIVATE_V4.test(ip)) ||
    (isIPv6(ip) && /^(fe80|fc|fd|::1$|::$)/i.test(ip));

  function setState(id, cls, text) {
    const el = $(id);
    el.className = "row-state " + cls;
    el.textContent = text;
  }
  function setVerdict(cls, kicker, title, note) {
    const v = $("verdict");
    v.className = "verdict " + cls;
    $("verdict-kicker").textContent = kicker;
    $("verdict-title").textContent = title;
    $("verdict-note").textContent = note;
  }

  async function lookupIp() {
    try {
      const r = await fetch(VLG.IP_API, { cache: "no-store" });
      const j = await r.json();
      if (j && j.ip) {
        return {
          ip: j.ip,
          isp: (j.connection && (j.connection.isp || j.connection.org)) || "",
          country: j.country || "",
          code: j.country_code || "",
          city: j.city || "",
          tz: (j.timezone && j.timezone.id) || ""
        };
      }
    } catch (e) {}
    try {
      const r = await fetch(VLG.IP_API_FALLBACK, { cache: "no-store" });
      const j = await r.json();
      return { ip: j.ip, isp: "", country: "", code: "", city: "", tz: "" };
    } catch (e) {
      return null;
    }
  }

  // Gather ICE candidates for ~2.5 s and return every IP they expose.
  function webrtcIps() {
    return new Promise((resolve) => {
      const found = new Map(); // ip -> type
      let pc;
      const done = () => {
        try { pc && pc.close(); } catch (e) {}
        resolve(found);
      };
      try {
        pc = new RTCPeerConnection({ iceServers: VLG.STUN });
      } catch (e) {
        return resolve(found);
      }
      pc.createDataChannel("vlg");
      pc.onicecandidate = (ev) => {
        if (!ev.candidate) return;
        const parts = ev.candidate.candidate.split(" ");
        // candidate:<foundation> <component> <proto> <priority> <ip> <port> typ <type> ...
        const ip = parts[4];
        const typ = parts[7] || "";
        if (!ip) return;
        if (ip.endsWith(".local")) { found.set(ip, "mdns"); return; }
        if (!found.has(ip)) found.set(ip, typ);
      };
      pc.createOffer().then((o) => pc.setLocalDescription(o)).catch(done);
      setTimeout(done, 2500);
    });
  }

  // DNS leak test through bash.ws: get a fresh id, make the browser resolve a few
  // random subdomains of it (the HTTPS requests fail, only the DNS lookup matters),
  // then read which resolvers asked bash.ws for those names.
  async function dnsLeakTest() {
    try {
      const id = (await (await fetch(VLG.DNS_API + "/id", { cache: "no-store" })).text()).trim();
      if (!/^[a-z0-9]{6,40}$/i.test(id)) return null;
      await Promise.all([1, 2, 3, 4, 5].map((n) =>
        Promise.race([
          fetch(`https://${n}.${id}.bash.ws/`, { mode: "no-cors", cache: "no-store" }).catch(() => {}),
          new Promise((r) => setTimeout(r, 2500))
        ])));
      const rows = await (await fetch(`${VLG.DNS_API}/dnsleak/test/${id}?json`, { cache: "no-store" })).json();
      if (!Array.isArray(rows)) return null;
      const dns = rows.filter((r) => r.type === "dns");
      const concl = (rows.find((r) => r.type === "conclusion") || {}).ip || "";
      return { dns, leaking: /may be leaking/i.test(concl), conclusion: concl };
    } catch (e) {
      return null;
    }
  }

  async function getPolicy() {
    try {
      const d = await chrome.privacy.network.webRTCIPHandlingPolicy.get({});
      return d;
    } catch (e) {
      return null;
    }
  }
  async function setBlock(on) {
    const value = on ? "disable_non_proxied_udp" : "default";
    await chrome.privacy.network.webRTCIPHandlingPolicy.set({ value });
  }

  async function runTest() {
    setVerdict("is-testing", "Scanning", "Testing your connection",
      "Public IP, WebRTC candidates and timezone are compared in your browser only.");
    ["ip", "webrtc", "dns", "tz"].forEach((k) => { setState(k + "-state", "", "…"); $(k + "-value").textContent = "…"; $(k + "-sub").textContent = ""; });
    $("fix").classList.add("hidden");

    const { homeIp = null } = await chrome.storage.local.get("homeIp");
    const [info, rtc, policy, dnsRes] = await Promise.all([lookupIp(), webrtcIps(), getPolicy(), dnsLeakTest()]);
    const blocking = policy && policy.value === "disable_non_proxied_udp";
    $("block-toggle").checked = !!blocking;

    // Public IP row
    if (!info) {
      setState("ip-state", "warn", "OFFLINE");
      $("ip-value").textContent = "No answer from the IP service";
      $("ip-sub").textContent = "Check your connection, then re-test.";
    } else {
      $("ip-value").textContent = info.ip;
      const where = [info.city, info.country].filter(Boolean).join(", ");
      $("ip-sub").textContent = [info.isp, where].filter(Boolean).join(" · ") || "What every website sees.";
      if (homeIp && info.ip === homeIp) setState("ip-state", "bad", "HOME IP");
      else if (homeIp) setState("ip-state", "ok", "NOT HOME");
      else setState("ip-state", "", "VISIBLE");
    }

    // WebRTC row
    const pub = [...rtc.entries()].filter(([ip, t]) => t !== "mdns" && !isPrivate(ip)).map(([ip]) => ip);
    const local = [...rtc.entries()].filter(([ip, t]) => t !== "mdns" && isPrivate(ip)).map(([ip]) => ip);
    const mdns = [...rtc.values()].filter((t) => t === "mdns").length;
    // Dual-stack: an IPv4 candidate next to an IPv6 public IP (or the reverse) is
    // the other address family of the same connection, not proof of a leak.
    const sameFamily = (x, y) => isIPv6(x) === isIPv6(y);
    const leaked = info ? pub.filter((ip) => ip !== info.ip && sameFamily(ip, info.ip)) : pub;
    const otherFamily = info ? pub.filter((ip) => ip !== info.ip && !sameFamily(ip, info.ip)) : [];
    const homeLeak = homeIp && pub.includes(homeIp) && (!info || info.ip !== homeIp);
    if (blocking) {
      // Chrome exempts extension pages from webRTCIPHandlingPolicy (measured
      // 2026-10-17): this probe still sees candidates while real websites get
      // none. Say so instead of pretending the probe is the proof.
      setState("webrtc-state", "ok", "BLOCKED ON SITES");
      $("webrtc-value").textContent = "Websites get no candidate";
      $("webrtc-sub").textContent = pub.length
        ? `Without blocking, WebRTC would expose ${pub.join(", ")}. Confirm from a real page with the full test below.`
        : "Chrome only lets WebRTC use the proxied route. Confirm from a real page with the full test below.";
    } else if (pub.length === 0) {
      setState("webrtc-state", "ok", "SILENT");
      $("webrtc-value").textContent = "No public candidate";
      $("webrtc-sub").textContent = mdns ? `Local addresses hidden by Chrome (${mdns} mDNS)` : "STUN returned nothing in 2.5 s.";
    } else if (leaked.length || homeLeak) {
      setState("webrtc-state", "bad", "LEAK");
      $("webrtc-value").textContent = (leaked.length ? leaked : pub).join(", ");
      $("webrtc-sub").textContent = "This address differs from your public IP: sites can read it through WebRTC.";
    } else if (otherFamily.length && !pub.includes(info.ip)) {
      setState("webrtc-state", "warn", isIPv6(info.ip) ? "IPV4 VISIBLE" : "IPV6 VISIBLE");
      $("webrtc-value").textContent = otherFamily.join(", ");
      $("webrtc-sub").textContent = "WebRTC shows your other address family. If your VPN does not cover it, sites see it: save your home IP or turn on blocking.";
    } else {
      setState("webrtc-state", "ok", "MATCH");
      $("webrtc-value").textContent = pub.join(", ");
      $("webrtc-sub").textContent = local.length ? `Also exposes local ${local.join(", ")}` : "Same address as your public IP.";
    }

    // DNS row
    let dnsLeak = false;
    if (!dnsRes) {
      setState("dns-state", "", "N/A");
      $("dns-value").textContent = "DNS test unavailable";
      $("dns-sub").textContent = "The bash.ws test did not answer. Re-test in a minute.";
    } else if (dnsRes.dns.length === 0) {
      setState("dns-state", "", "N/A");
      $("dns-value").textContent = "No resolver seen";
      $("dns-sub").textContent = dnsRes.conclusion || "Re-test in a minute.";
    } else {
      const orgs = [...new Set(dnsRes.dns.map((d) => [d.org || d.asn, (d.country || "").toUpperCase()].filter(Boolean).join(" ")))];
      $("dns-value").textContent = `${dnsRes.dns.length} resolver${dnsRes.dns.length > 1 ? "s" : ""}: ${orgs.slice(0, 2).join(", ")}${orgs.length > 2 ? "…" : ""}`;
      dnsLeak = dnsRes.leaking;
      if (dnsLeak) {
        setState("dns-state", "bad", "LEAK");
        $("dns-sub").textContent = "Your DNS requests go to a resolver outside your VPN: your provider can see the sites you visit.";
      } else {
        setState("dns-state", "ok", "NO LEAK");
        $("dns-sub").textContent = "Resolvers match your connection. " + (dnsRes.conclusion || "");
      }
    }

    // Timezone row
    const browserTz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
    $("tz-value").textContent = browserTz || "unknown";
    if (info && info.tz && browserTz) {
      const sameOffset = tzOffsetMinutes(browserTz) === tzOffsetMinutes(info.tz);
      if (sameOffset) {
        setState("tz-state", "ok", "CONSISTENT");
        $("tz-sub").textContent = `IP timezone ${info.tz}`;
      } else {
        setState("tz-state", "warn", "MISMATCH");
        $("tz-sub").textContent = `IP says ${info.tz}. Fingerprinting scripts can flag a VPN from this.`;
      }
    } else {
      setState("tz-state", "", "N/A");
      $("tz-sub").textContent = "IP timezone unavailable.";
    }

    // Verdict
    const homeExposed = !!(homeIp && info && info.ip === homeIp);
    if (dnsLeak && !(!blocking && (leaked.length || homeLeak))) {
      setVerdict("is-bad", "Leak detected", "DNS requests leave your VPN",
        "Your DNS resolver can log every site you open. Use a VPN with its own DNS and leak protection.");
      $("fix").classList.remove("hidden");
    } else if (!blocking && (leaked.length || homeLeak)) {
      setVerdict("is-bad", "Leak detected", "WebRTC reveals another IP",
        "Websites can read an address your VPN is supposed to hide. Turn on blocking below, or use a VPN that blocks WebRTC.");
      $("fix").classList.remove("hidden");
    } else if (homeExposed) {
      setVerdict("is-bad", "VPN off", "Your home IP is visible",
        "Your public IP equals the home IP you saved. Connect your VPN, then re-test.");
      $("fix").classList.remove("hidden");
    } else if (!info) {
      setVerdict("is-warn", "Incomplete", "Could not read your public IP",
        "The WebRTC part ran, but without a public IP the comparison is partial.");
    } else if (blocking) {
      setVerdict("is-ok", "Protected", "WebRTC blocked on websites",
        "Chrome restricts WebRTC to the proxied route on every site. Keep it on while you use a VPN.");
    } else if (pub.length === 0) {
      setVerdict("is-ok", "Protected", "No WebRTC leak",
        "No public address came back through WebRTC. Blocking is still recommended on a VPN.");
    } else if (!homeIp) {
      setVerdict("is-warn", "Unverified", "WebRTC matches your public IP",
        "Fine if you are on a VPN. If this is your home IP, save it below so the guard can tell the difference.");
    } else {
      setVerdict("is-ok", "Protected", "No WebRTC leak",
        "WebRTC only shows your VPN address, and it is not your home IP.");
    }
    await chrome.storage.local.set({ lastTest: { at: Date.now(), ip: info && info.ip, leak: !blocking && (leaked.length > 0 || !!homeLeak), dnsLeak } });
    return info;
  }

  function tzOffsetMinutes(tz) {
    try {
      const now = new Date();
      const fmt = new Intl.DateTimeFormat("en-US", { timeZone: tz, hour12: false, year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" });
      const p = Object.fromEntries(fmt.formatToParts(now).map((x) => [x.type, x.value]));
      const asUtc = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour % 24, +p.minute);
      return Math.round((asUtc - now.setSeconds(0, 0)) / 60000);
    } catch (e) { return NaN; }
  }

  // Controls
  $("block-toggle").addEventListener("change", async (ev) => {
    try {
      await setBlock(ev.target.checked);
      $("block-help").textContent = ev.target.checked
        ? "On. Chrome now routes WebRTC through your proxy or VPN only."
        : "Off. Chrome uses its default WebRTC routing.";
      setTimeout(runTest, 300);
    } catch (e) {
      ev.target.checked = !ev.target.checked;
      $("block-help").textContent = "Chrome refused the change (another extension or a policy controls this setting).";
    }
  });

  async function refreshHomeHint() {
    const { homeIp = null, homeSetAt = 0 } = await chrome.storage.local.get(["homeIp", "homeSetAt"]);
    if (homeIp) {
      $("home-hint").textContent = `Home IP saved: ${homeIp} (${new Date(homeSetAt).toLocaleDateString()}). Click again to replace it.`;
      $("set-home").textContent = "Update my home IP (I am not on a VPN right now)";
    } else {
      $("home-hint").textContent = "Save it once while your VPN is off: the guard can then prove your VPN hides it.";
    }
  }
  $("set-home").addEventListener("click", async () => {
    const info = await lookupIp();
    if (!info) { $("home-hint").textContent = "Could not read your IP right now."; return; }
    await chrome.storage.local.set({ homeIp: info.ip, homeSetAt: Date.now() });
    await refreshHomeHint();
    runTest();
  });

  // VPN drop alerts (free)
  async function refreshPro() {
    const { watchEnabled = false, homeIp = null } = await chrome.storage.local.get(["watchEnabled", "homeIp"]);
    $("watch-toggle").checked = !!watchEnabled;
    $("pro-text").textContent = homeIp
      ? "Background check every 2 minutes. You get a notification if your public IP falls back to your home IP."
      : "Save your home IP above first: the watch compares against it.";
  }
  $("watch-toggle").addEventListener("change", async (ev) => {
    await chrome.storage.local.set({ watchEnabled: ev.target.checked });
  });

  $("rerun").addEventListener("click", runTest);

  refreshHomeHint();
  refreshPro();
  runTest();
})();
