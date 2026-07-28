"use client";

import { useEffect, useState } from "react";

function urlBase64ToUint8Array(base64: string) {
  const padding = "=".repeat((4 - (base64.length % 4)) % 4);
  const b64 = (base64 + padding).replace(/-/g, "+").replace(/_/g, "/");
  const raw = atob(b64);
  const arr = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; ++i) arr[i] = raw.charCodeAt(i);
  return arr;
}

type State =
  | { kind: "unsupported" }
  | { kind: "denied" }
  | { kind: "granted-idle" }
  | { kind: "granted-subscribed" }
  | { kind: "default" }
  | { kind: "not-standalone-ios" };

export default function EnableNotifications() {
  const [state, setState] = useState<State>({ kind: "default" });
  const [busy, setBusy] = useState(false);
  const [note, setNote] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      if (typeof window === "undefined") return;

      const isIos = /iPad|iPhone|iPod/.test(navigator.userAgent);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const isStandalone = (window.matchMedia?.("(display-mode: standalone)").matches) || (window.navigator as any).standalone;

      if (!("Notification" in window) || !("serviceWorker" in navigator) || !("PushManager" in window)) {
        setState({ kind: "unsupported" });
        return;
      }
      if (isIos && !isStandalone) {
        setState({ kind: "not-standalone-ios" });
        return;
      }
      if (Notification.permission === "denied") {
        setState({ kind: "denied" });
        return;
      }
      if (Notification.permission === "granted") {
        const reg = await navigator.serviceWorker.getRegistration();
        const sub = await reg?.pushManager.getSubscription();
        setState({ kind: sub ? "granted-subscribed" : "granted-idle" });
        return;
      }
      setState({ kind: "default" });
    })();
  }, []);

  async function enable() {
    setBusy(true);
    setNote(null);
    try {
      const publicKey = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY;
      if (!publicKey) {
        setNote("push not configured on the server yet.");
        setBusy(false);
        return;
      }

      // 1. Register the service worker (idempotent)
      const reg = await navigator.serviceWorker.register("/sw.js");
      await navigator.serviceWorker.ready;

      // 2. Ask for permission
      const perm = await Notification.requestPermission();
      if (perm !== "granted") {
        setState({ kind: perm === "denied" ? "denied" : "default" });
        setBusy(false);
        return;
      }

      // 3. Subscribe
      const sub =
        (await reg.pushManager.getSubscription()) ||
        (await reg.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array(publicKey),
        }));

      // 4. Send subscription to server
      const raw = sub.toJSON();
      const r = await fetch("/api/push/subscribe", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          endpoint: raw.endpoint,
          keys: raw.keys,
          userAgent: navigator.userAgent,
        }),
      });
      if (!r.ok) {
        const j = await r.json().catch(() => ({}));
        throw new Error(j.error || "server rejected subscription");
      }

      setState({ kind: "granted-subscribed" });
      setNote("notifications on ♥");
    } catch (err: any) {
      setNote(err?.message || "couldn't enable notifications");
    } finally {
      setBusy(false);
    }
  }

  async function disable() {
    setBusy(true);
    try {
      const reg = await navigator.serviceWorker.getRegistration();
      const sub = await reg?.pushManager.getSubscription();
      if (sub) {
        await fetch("/api/push/subscribe", {
          method: "DELETE",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ endpoint: sub.endpoint }),
        });
        await sub.unsubscribe();
      }
      setState({ kind: "granted-idle" });
      setNote("notifications off");
    } finally {
      setBusy(false);
    }
  }

  if (state.kind === "unsupported") {
    return (
      <div className="px-4 py-2 text-[10px] tracking-widest2 uppercase text-ink-mute bg-ink/5 text-center">
        this browser can&apos;t do push notifications.
      </div>
    );
  }
  if (state.kind === "not-standalone-ios") {
    return (
      <div className="px-4 py-2 text-[10px] tracking-widest2 uppercase text-ink-soft bg-rose-wash/40 text-center leading-snug">
        add to home screen first (share → add to home screen), then reopen from there for notifications.
      </div>
    );
  }
  if (state.kind === "denied") {
    return (
      <div className="px-4 py-2 text-[10px] tracking-widest2 uppercase text-rose-deep bg-rose-wash/40 text-center leading-snug">
        notifications blocked. enable in browser/system settings.
      </div>
    );
  }
  if (state.kind === "granted-subscribed") {
    return (
      <div className="px-4 py-2 flex items-center justify-between gap-2 text-[10px] tracking-widest2 uppercase text-ink-soft bg-ink/5">
        <span>notifications on ♥</span>
        <button onClick={disable} disabled={busy} className="underline underline-offset-2 hover:text-ink">
          {busy ? "…" : "turn off"}
        </button>
      </div>
    );
  }
  return (
    <div className="px-4 py-2 flex items-center justify-between gap-2 text-[10px] tracking-widest2 uppercase text-ink-soft bg-ivory">
      <span>{note || "get notified when a note arrives"}</span>
      <button
        onClick={enable}
        disabled={busy}
        className="underline underline-offset-2 hover:text-ink"
      >
        {busy ? "…" : "enable"}
      </button>
    </div>
  );
}
