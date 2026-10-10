"use strict";

// ---- Pairing token -------------------------------------------------------
// The QR code opens "/?t=TOKEN". Keep the token and drop it from the address
// bar, so a home-screen shortcut created afterwards still works.
const TOKEN_STORAGE = "pc-remote-token";

function readToken() {
  const fromUrl = new URLSearchParams(location.search).get("t");
  if (fromUrl) {
    try { localStorage.setItem(TOKEN_STORAGE, fromUrl); } catch (_) {}
    history.replaceState(null, "", location.pathname);
    return fromUrl;
  }
  try { return localStorage.getItem(TOKEN_STORAGE); } catch (_) { return null; }
}

const token = readToken();
const statusEl = document.getElementById("status");

// ---- Connection ----------------------------------------------------------
let ws = null;
let retryDelay = 500;
let everOpened = false;

function setStatus(text, ok) {
  statusEl.textContent = text;
  statusEl.classList.toggle("status--on", ok);
  statusEl.classList.toggle("status--off", !ok);
}

function connect() {
  const proto = location.protocol === "https:" ? "wss:" : "ws:";
  ws = new WebSocket(`${proto}//${location.host}/ws?t=${encodeURIComponent(token)}`);
  setStatus("Подключение…", false);

  ws.onopen = () => {
    retryDelay = 500;
    everOpened = true;
    setStatus("ПК подключён", true);
  };
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === "error") console.warn("PC:", msg.message);
  };
  ws.onclose = async () => {
    ws = null;
    setStatus("Нет связи, переподключаюсь…", false);
    // The browser hides why a WebSocket failed; ask the PC whether the token
    // is still valid so a stale pairing shows the pairing screen instead of looping.
    if (!everOpened && await tokenRejected()) {
      showPairing();
      return;
    }
    setTimeout(connect, retryDelay);
    retryDelay = Math.min(retryDelay * 2, 5000);
  };
}

async function tokenRejected() {
  try {
    const res = await fetch(`/check?t=${encodeURIComponent(token)}`, { cache: "no-store" });
    return res.status === 401;
  } catch (_) {
    return false; // PC unreachable: keep retrying.
  }
}

function showPairing() {
  document.getElementById("pair").hidden = false;
  setStatus("Нет ключа", false);
}

function send(msg) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(msg));
    return true;
  }
  return false;
}

function buzz() {
  if (navigator.vibrate) navigator.vibrate(12);
}

// Reconnect right away when the phone wakes up or the app comes back.
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "visible") {
    if (!ws) connect();
    requestWakeLock();
  }
});

// ---- Buttons -------------------------------------------------------------
// data-action: named action, data-keys: key combo ("shift+n"), data-click: mouse button.
// data-repeat: keep firing while held (seek, volume, arrows).
function messageFor(btn) {
  if (btn.dataset.action) return { type: "action", name: btn.dataset.action };
  if (btn.dataset.keys) return { type: "key", keys: btn.dataset.keys.split("+") };
  if (btn.dataset.click) return { type: "click", button: btn.dataset.click };
  return null;
}

function bindButton(btn) {
  const msg = messageFor(btn);
  if (!msg) return;
  let holdTimer = null;
  let repeatTimer = null;

  const stop = () => {
    clearTimeout(holdTimer);
    clearInterval(repeatTimer);
    holdTimer = repeatTimer = null;
    btn.classList.remove("btn--pressed");
  };

  btn.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    btn.classList.add("btn--pressed");
    if (send(msg)) buzz();
    if ("repeat" in btn.dataset) {
      holdTimer = setTimeout(() => {
        repeatTimer = setInterval(() => send(msg), 180);
      }, 450);
    }
  });
  btn.addEventListener("pointerup", stop);
  btn.addEventListener("pointercancel", stop);
  btn.addEventListener("pointerleave", stop);
  btn.addEventListener("contextmenu", (e) => e.preventDefault());
}

document.querySelectorAll("main button[data-action], main button[data-keys], main button[data-click]")
  .forEach(bindButton);

// ---- Tabs ----------------------------------------------------------------
document.querySelectorAll(".tabbar__item").forEach((item) => {
  item.addEventListener("click", () => {
    document.querySelectorAll(".tabbar__item").forEach((i) => i.classList.toggle("tabbar__item--active", i === item));
    document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("tab--active", t.id === `tab-${item.dataset.tab}`));
  });
});

// ---- Text input ----------------------------------------------------------
const textInput = document.getElementById("text");
document.getElementById("text-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const text = textInput.value;
  if (text && send({ type: "text", text })) {
    buzz();
    textInput.value = "";
  }
});

// ---- Touchpad ------------------------------------------------------------
const pad = document.getElementById("pad");
const sensInput = document.getElementById("sens");
const SENS_STORAGE = "pc-remote-sens";
try { sensInput.value = localStorage.getItem(SENS_STORAGE) || sensInput.value; } catch (_) {}
sensInput.addEventListener("change", () => {
  try { localStorage.setItem(SENS_STORAGE, sensInput.value); } catch (_) {}
});

const touches = new Map();
let gesture = null; // {start, fingers, moved, lastY}
let pending = { dx: 0, dy: 0, scroll: 0 };
let frameQueued = false;

function flush() {
  frameQueued = false;
  const dx = Math.round(pending.dx);
  const dy = Math.round(pending.dy);
  if (dx || dy) {
    send({ type: "move", dx, dy });
    pending.dx -= dx;
    pending.dy -= dy;
  }
  const steps = Math.trunc(pending.scroll / 25);
  if (steps) {
    send({ type: "scroll", dx: 0, dy: steps });
    pending.scroll -= steps * 25;
  }
}

function queueFlush() {
  if (!frameQueued) {
    frameQueued = true;
    requestAnimationFrame(flush);
  }
}

pad.addEventListener("pointerdown", (e) => {
  e.preventDefault();
  pad.setPointerCapture(e.pointerId);
  touches.set(e.pointerId, { x: e.clientX, y: e.clientY });
  if (!gesture) gesture = { start: performance.now(), fingers: 0, moved: 0 };
  gesture.fingers = Math.max(gesture.fingers, touches.size);
});

pad.addEventListener("pointermove", (e) => {
  const prev = touches.get(e.pointerId);
  if (!prev) return;
  const dx = e.clientX - prev.x;
  const dy = e.clientY - prev.y;
  touches.set(e.pointerId, { x: e.clientX, y: e.clientY });
  gesture.moved += Math.abs(dx) + Math.abs(dy);

  if (touches.size >= 2) {
    // Two-finger drag scrolls like on the phone itself: finger up, page down.
    // Each finger reports its own move, so average them.
    pending.scroll += dy / touches.size;
  } else {
    // Faster finger movement moves the cursor disproportionately further.
    const speed = Math.hypot(dx, dy);
    const accel = Number(sensInput.value) * (1 + Math.min(speed, 40) / 20);
    pending.dx += dx * accel;
    pending.dy += dy * accel;
  }
  queueFlush();
});

function endPointer(e) {
  if (!touches.delete(e.pointerId) || touches.size > 0 || !gesture) return;
  const isTap = performance.now() - gesture.start < 250 && gesture.moved < 12;
  if (isTap && send({ type: "click", button: gesture.fingers >= 2 ? "right" : "left" })) buzz();
  gesture = null;
}
pad.addEventListener("pointerup", endPointer);
pad.addEventListener("pointercancel", endPointer);

// ---- Keep the screen on --------------------------------------------------
// On a treadmill the phone should not lock between taps. The Wake Lock API
// needs a secure context; over plain http on the LAN some browsers lack it.
const wakeBtn = document.getElementById("wake");
let wakeLock = null;
let wakeWanted = true;

async function requestWakeLock() {
  if (!wakeWanted || wakeLock || !("wakeLock" in navigator)) return updateWakeBtn();
  try {
    wakeLock = await navigator.wakeLock.request("screen");
    wakeLock.addEventListener("release", () => { wakeLock = null; updateWakeBtn(); });
  } catch (_) {
    wakeLock = null;
  }
  updateWakeBtn();
}

function updateWakeBtn() {
  if (!("wakeLock" in navigator)) {
    wakeBtn.textContent = "Экран: как в системе";
    wakeBtn.disabled = true;
    return;
  }
  wakeBtn.textContent = wakeLock ? "Экран не гаснет" : "Экран: авто";
  wakeBtn.setAttribute("aria-pressed", String(Boolean(wakeLock)));
}

wakeBtn.addEventListener("click", async () => {
  wakeWanted = !wakeLock;
  if (wakeLock) await wakeLock.release();
  else await requestWakeLock();
});

// The browser only grants a wake lock after a user gesture.
document.addEventListener("pointerdown", () => requestWakeLock(), { once: true });

// ---- Start ---------------------------------------------------------------
if (token) {
  connect();
  updateWakeBtn();
} else {
  showPairing();
}
