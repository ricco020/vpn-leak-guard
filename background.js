// Service worker: Pro "VPN drop" watch + ExtPay bootstrap.
importScripts("config.js", "vendor/ExtPay.js");

const extpay = ExtPay(VLG.EXTPAY_ID);
try {
  extpay.startBackground();
} catch (e) {
  // ExtPay not registered yet: the extension keeps working in free mode.
}

const ALARM = "vlg-watch";

async function getPublicIp() {
  try {
    const r = await fetch(VLG.IP_API, { cache: "no-store" });
    const j = await r.json();
    if (j && j.ip) return j.ip;
  } catch (e) {}
  try {
    const r = await fetch(VLG.IP_API_FALLBACK, { cache: "no-store" });
    const j = await r.json();
    return j.ip || null;
  } catch (e) {
    return null;
  }
}

async function isPaid() {
  if (VLG.PRO_FREE) return true;
  try {
    const u = await extpay.getUser();
    return !!(u && u.paid);
  } catch (e) {
    return false;
  }
}

async function applyWatchState() {
  const { watchEnabled = false, watchMinutes = VLG.WATCH_MINUTES_DEFAULT, homeIp = null } =
    await chrome.storage.local.get(["watchEnabled", "watchMinutes", "homeIp"]);
  const paid = await isPaid();
  await chrome.alarms.clear(ALARM);
  if (watchEnabled && paid && homeIp) {
    chrome.alarms.create(ALARM, { periodInMinutes: Math.max(1, Number(watchMinutes) || 2) });
  }
}

chrome.runtime.onInstalled.addListener(() => {
  applyWatchState();
});
chrome.runtime.onStartup.addListener(() => {
  applyWatchState();
});
chrome.storage.onChanged.addListener((changes, area) => {
  if (area !== "local") return;
  if (changes.watchEnabled || changes.watchMinutes || changes.homeIp) applyWatchState();
});

chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name !== ALARM) return;
  const { homeIp, lastWatchIp = null, lastAlertAt = 0 } = await chrome.storage.local.get([
    "homeIp",
    "lastWatchIp",
    "lastAlertAt"
  ]);
  const ip = await getPublicIp();
  if (!ip) return;
  const exposed = homeIp && ip === homeIp;
  const wasExposed = homeIp && lastWatchIp === homeIp;
  await chrome.storage.local.set({ lastWatchIp: ip, lastWatchAt: Date.now() });
  // Alert on the transition to the home IP, and at most once every 10 minutes while it lasts.
  if (exposed && (!wasExposed || Date.now() - lastAlertAt > 10 * 60 * 1000)) {
    await chrome.storage.local.set({ lastAlertAt: Date.now() });
    chrome.notifications.create("vlg-drop-" + Date.now(), {
      type: "basic",
      iconUrl: "icons/icon-128.png",
      title: "VPN Leak Guard: your real IP is visible",
      message: `Your public IP (${ip}) is the home IP you saved. Your VPN looks disconnected.`,
      priority: 2
    });
    chrome.action.setBadgeText({ text: "!" });
    chrome.action.setBadgeBackgroundColor({ color: "#FF6A3D" });
  } else if (!exposed) {
    chrome.action.setBadgeText({ text: "" });
  }
});
