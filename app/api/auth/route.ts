import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  const { password } = await req.json().catch(() => ({}));

  const pwMe = process.env.PASSWORD_ME;
  const pwDiya = process.env.PASSWORD_DIYA;

  if (!pwMe || !pwDiya) {
    return NextResponse.json(
      { ok: false, error: "Server not configured (PASSWORD_ME / PASSWORD_DIYA missing)." },
      { status: 500 }
    );
  }
  if (typeof password !== "string" || !password) {
    return NextResponse.json({ ok: false, error: "Password required" }, { status: 400 });
  }

  let identity: "me" | "diya" | null = null;
  if (password === pwMe) identity = "me";
  else if (password === pwDiya) identity = "diya";

  if (!identity) {
    return NextResponse.json({ ok: false, error: "Wrong password" }, { status: 401 });
  }

  const res = NextResponse.json({ ok: true, identity });
  const oneYear = 60 * 60 * 24 * 365;
  const cookieOpts = {
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax" as const,
    path: "/",
    maxAge: oneYear,
  };
  res.cookies.set("chat_auth", "1", { ...cookieOpts, httpOnly: true });
  res.cookies.set("chat_identity", identity, { ...cookieOpts, httpOnly: true });
  // Non-http cookie so the client knows who it is (without exposing auth)
  res.cookies.set("chat_who", identity, { ...cookieOpts, httpOnly: false });
  return res;
}

export async function DELETE() {
  const res = NextResponse.json({ ok: true });
  res.cookies.delete("chat_auth");
  res.cookies.delete("chat_identity");
  res.cookies.delete("chat_who");
  return res;
}
