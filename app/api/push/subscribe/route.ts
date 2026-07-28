import { NextRequest, NextResponse } from "next/server";
import { getSupabaseServer } from "@/lib/supabase-server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

function requireAuth(req: NextRequest) {
  const auth = req.cookies.get("chat_auth")?.value;
  const identity = req.cookies.get("chat_identity")?.value;
  if (auth !== "1" || (identity !== "diya" && identity !== "me")) return null;
  return identity as "diya" | "me";
}

export async function POST(req: NextRequest) {
  const who = requireAuth(req);
  if (!who) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const body = await req.json().catch(() => ({}));
  const { endpoint, keys, userAgent } = body || {};
  if (!endpoint || !keys?.p256dh || !keys?.auth) {
    return NextResponse.json({ error: "invalid subscription" }, { status: 400 });
  }

  const supabase = getSupabaseServer();
  // Upsert on endpoint so re-subscribing on same device just updates keys
  const { error } = await supabase
    .from("push_subscriptions")
    .upsert(
      {
        identity: who,
        endpoint,
        p256dh: keys.p256dh,
        auth: keys.auth,
        user_agent: typeof userAgent === "string" ? userAgent.slice(0, 300) : null,
      },
      { onConflict: "endpoint" }
    );

  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true });
}

export async function DELETE(req: NextRequest) {
  const who = requireAuth(req);
  if (!who) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const body = await req.json().catch(() => ({}));
  const { endpoint } = body || {};
  if (!endpoint) return NextResponse.json({ error: "missing endpoint" }, { status: 400 });

  const supabase = getSupabaseServer();
  await supabase.from("push_subscriptions").delete().eq("endpoint", endpoint);
  return NextResponse.json({ ok: true });
}
