/* Service worker — handles Web Push and click-through */

self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("push", (event) => {
  let data = { title: "For Diya", body: "you have a new note", url: "/" };
  try {
    if (event.data) data = { ...data, ...event.data.json() };
  } catch (e) {
    // if payload isn't JSON, fall back to text
    try { data.body = event.data.text(); } catch {}
  }

  const options = {
    body: data.body,
    icon: "/icon.svg",
    badge: "/icon.svg",
    data: { url: data.url || "/" },
    tag: data.tag || "diya-chat",
    renotify: true,
    vibrate: [80, 40, 80],
  };

  event.waitUntil(self.registration.showNotification(data.title, options));
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  const url = (event.notification.data && event.notification.data.url) || "/";
  event.waitUntil(
    self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((wins) => {
      // If a tab is already open, focus it
      for (const w of wins) {
        if ("focus" in w) return w.focus();
      }
      if (self.clients.openWindow) return self.clients.openWindow(url);
    })
  );
});
