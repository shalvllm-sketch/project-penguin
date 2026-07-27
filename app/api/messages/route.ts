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

export async function GET(req: NextRequest) {
  const who = requireAuth(req);
  if (!who) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const url = new URL(req.url);
  const sinceParam = url.searchParams.get("since");
  const supabase = getSupabaseServer();

  let q = supabase
    .from("messages")
    .select("id, sender, content, created_at")
    .order("created_at", { ascending: true })
    .limit(500);

  if (sinceParam) q = q.gt("created_at", sinceParam);

  const { data, error } = await q;
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ messages: data ?? [] });
}

export async function POST(req: NextRequest) {
  const who = requireAuth(req);
  if (!who) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const body = await req.json().catch(() => ({}));
  const content = typeof body?.content === "string" ? body.content.trim() : "";
  if (!content) return NextResponse.json({ error: "empty" }, { status: 400 });
  if (content.length > 2000) return NextResponse.json({ error: "too long" }, { status: 400 });

  const supabase = getSupabaseServer();
  const { data, error } = await supabase
    .from("messages")
    .insert({ sender: who, content })
    .select("id, sender, content, created_at")
    .single();

  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ message: data });
}
