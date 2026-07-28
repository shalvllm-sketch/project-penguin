import webpush from "web-push";
import { getSupabaseServer } from "@/lib/supabase-server";

let configured = false;

function configure() {
  if (configured) return true;
  const publicKey = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY;
  const privateKey = process.env.VAPID_PRIVATE_KEY;
  const subject = process.env.VAPID_SUBJECT || "mailto:you@example.com";
  if (!publicKey || !privateKey) return false;
  webpush.setVapidDetails(subject, publicKey, privateKey);
  configured = true;
  return true;
}

/**
 * Send a push notification to every device belonging to `identity`.
 * Silently drops dead subscriptions (404/410 responses from browser push endpoints).
 */
export async function pushTo(
  identity: "diya" | "me",
  payload: { title: string; body: string; url?: string; tag?: string }
) {
  if (!configure()) return { sent: 0, reason: "VAPID keys not configured" };

  const supabase = getSupabaseServer();
  const { data: subs, error } = await supabase
    .from("push_subscriptions")
    .select("id, endpoint, p256dh, auth")
    .eq("identity", identity);

  if (error) return { sent: 0, reason: error.message };
  if (!subs || subs.length === 0) return { sent: 0, reason: "no subscriptions" };

  const body = JSON.stringify(payload);
  let sent = 0;
  const deadIds: string[] = [];

  await Promise.all(
    subs.map(async (s) => {
      const sub = {
        endpoint: s.endpoint,
        keys: { p256dh: s.p256dh, auth: s.auth },
      };
      try {
        await webpush.sendNotification(sub, body, { TTL: 60 });
        sent += 1;
      } catch (err: any) {
        const status = err?.statusCode;
        if (status === 404 || status === 410) deadIds.push(s.id);
      }
    })
  );

  if (deadIds.length) {
    await supabase.from("push_subscriptions").delete().in("id", deadIds);
  }

  return { sent, reason: sent ? "ok" : "no delivery" };
}
