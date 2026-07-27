"use client";

import { useEffect, useRef, useState } from "react";

type Msg = {
  id: string;
  sender: "diya" | "me";
  content: string;
  created_at: string;
};

function getCookie(name: string) {
  if (typeof document === "undefined") return null;
  const m = document.cookie.match(new RegExp("(?:^|; )" + name + "=([^;]*)"));
  return m ? decodeURIComponent(m[1]) : null;
}

function formatTime(iso: string) {
  const d = new Date(iso);
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function sameDay(a: string, b: string) {
  const da = new Date(a), db = new Date(b);
  return da.toDateString() === db.toDateString();
}

function dayLabel(iso: string) {
  const d = new Date(iso);
  const today = new Date();
  const yest = new Date(); yest.setDate(today.getDate() - 1);
  if (d.toDateString() === today.toDateString()) return "Today";
  if (d.toDateString() === yest.toDateString()) return "Yesterday";
  return d.toLocaleDateString([], { weekday: "long", month: "short", day: "numeric" });
}

export default function ChatPanel({ onClose }: { onClose: () => void }) {
  const [identity, setIdentity] = useState<"diya" | "me" | null>(null);
  const [needsAuth, setNeedsAuth] = useState(true);
  const [password, setPassword] = useState("");
  const [authError, setAuthError] = useState<string | null>(null);
  const [authing, setAuthing] = useState(false);

  const [messages, setMessages] = useState<Msg[]>([]);
  const [text, setText] = useState("");
  const [sending, setSending] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [sendError, setSendError] = useState<string | null>(null);

  const scrollRef = useRef<HTMLDivElement>(null);
  const lastFetchRef = useRef<string | null>(null);

  useEffect(() => {
    const who = getCookie("chat_who");
    if (who === "diya" || who === "me") {
      setIdentity(who);
      setNeedsAuth(false);
    }
  }, []);

  useEffect(() => {
    if (needsAuth || !identity) return;
    let cancelled = false;

    const fetchInitial = async () => {
      try {
        const r = await fetch("/api/messages", { cache: "no-store" });
        if (r.status === 401) { setNeedsAuth(true); return; }
        const j = await r.json();
        if (cancelled) return;
        setMessages(j.messages ?? []);
        if (j.messages?.length) lastFetchRef.current = j.messages[j.messages.length - 1].created_at;
      } catch (e: any) {
        setLoadError("Couldn't load messages");
      }
    };

    fetchInitial();

    const id = setInterval(async () => {
      try {
        const since = lastFetchRef.current;
        const url = since ? `/api/messages?since=${encodeURIComponent(since)}` : "/api/messages";
        const r = await fetch(url, { cache: "no-store" });
        if (r.status === 401) { setNeedsAuth(true); return; }
        const j = await r.json();
        if (cancelled || !j.messages?.length) return;
        setMessages((prev) => {
          const existing = new Set(prev.map((m) => m.id));
          const fresh = j.messages.filter((m: Msg) => !existing.has(m.id));
          if (!fresh.length) return prev;
          lastFetchRef.current = fresh[fresh.length - 1].created_at;
          return [...prev, ...fresh];
        });
      } catch {
        /* ignore transient errors */
      }
    }, 2000);

    return () => { cancelled = true; clearInterval(id); };
  }, [needsAuth, identity]);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages]);

  async function handleAuth(e: React.FormEvent) {
    e.preventDefault();
    setAuthing(true);
    setAuthError(null);
    try {
      const r = await fetch("/api/auth", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ password }),
      });
      const j = await r.json();
      if (!r.ok) throw new Error(j.error || "Something went wrong");
      setIdentity(j.identity);
      setNeedsAuth(false);
      setPassword("");
    } catch (err: any) {
      setAuthError(err.message || "Try again");
    } finally {
      setAuthing(false);
    }
  }

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    const content = text.trim();
    if (!content || sending) return;
    setSending(true);
    setSendError(null);

    // Optimistic message
    const tempId = "temp-" + Math.random().toString(36).slice(2);
    const optimistic: Msg = {
      id: tempId,
      sender: identity!,
      content,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, optimistic]);
    setText("");

    try {
      const r = await fetch("/api/messages", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ content }),
      });
      if (r.status === 401) { setNeedsAuth(true); return; }
      const j = await r.json();
      if (!r.ok) throw new Error(j.error || `send failed (${r.status})`);
      setMessages((prev) =>
        prev.map((m) => (m.id === tempId ? j.message : m))
      );
      lastFetchRef.current = j.message.created_at;
    } catch (err: any) {
      setMessages((prev) => prev.filter((m) => m.id !== tempId));
      setText(content); // put it back so they can retry
      setSendError(err?.message || "couldn't send — try again");
    } finally {
      setSending(false);
    }
  }

  async function handleLogout() {
    await fetch("/api/auth", { method: "DELETE" });
    setIdentity(null);
    setNeedsAuth(true);
    setMessages([]);
  }

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/30 backdrop-blur-sm p-0 sm:p-6 animate-fade-in">
      <div className="w-full sm:max-w-md h-[90vh] sm:h-[600px] bg-white rounded-t-3xl sm:rounded-3xl shadow-2xl overflow-hidden flex flex-col animate-pop-in border border-blush-100">
        {/* Header */}
        <div className="bg-gradient-to-r from-blush-300 to-peach-300 px-4 py-3 flex items-center gap-3 text-white">
          <div className="w-10 h-10 rounded-full bg-white/30 flex items-center justify-center text-xl backdrop-blur-sm">
            💕
          </div>
          <div className="flex-1 min-w-0">
            <div className="font-semibold serif text-lg leading-tight">Us</div>
            <div className="text-xs opacity-90">
              {identity ? `signed in as ${identity === "diya" ? "Diya" : "you"}` : "our little chat"}
            </div>
          </div>
          {identity && (
            <button
              onClick={handleLogout}
              className="text-xs opacity-80 hover:opacity-100 underline underline-offset-2"
              aria-label="log out"
            >
              logout
            </button>
          )}
          <button
            onClick={onClose}
            className="w-9 h-9 rounded-full hover:bg-white/20 flex items-center justify-center text-xl"
            aria-label="close chat"
          >
            ×
          </button>
        </div>

        {needsAuth ? (
          <form onSubmit={handleAuth} className="flex-1 flex flex-col items-center justify-center gap-4 p-6 bg-cream">
            <div className="text-5xl">🔐</div>
            <p className="serif text-xl text-blush-400 text-center">
              tell me the secret word 💌
            </p>
            <p className="text-xs text-peach-400 text-center max-w-[220px] -mt-2">
              your password decides who you are — no need to pick a side.
            </p>
            <input
              type="password"
              autoFocus
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="secret word..."
              className="w-full max-w-xs px-4 py-3 rounded-2xl bg-white border border-blush-100 focus:outline-none focus:border-blush-300 text-center"
            />
            {authError && <p className="text-xs text-rose-500">{authError}</p>}
            <button
              type="submit"
              disabled={authing || !password}
              className="px-6 py-2 rounded-full bg-gradient-to-r from-blush-300 to-peach-300 text-white font-semibold shadow-md disabled:opacity-50"
            >
              {authing ? "opening..." : "open"}
            </button>
          </form>
        ) : (
          <>
            {/* Messages */}
            <div
              ref={scrollRef}
              className="chat-scroll flex-1 overflow-y-auto px-3 py-4 bg-gradient-to-b from-blush-50 to-peach-50 space-y-1"
            >
              {loadError && (
                <p className="text-center text-xs text-rose-400">{loadError}</p>
              )}
              {messages.length === 0 && !loadError && (
                <div className="h-full flex flex-col items-center justify-center text-blush-300 gap-2">
                  <div className="text-4xl">💌</div>
                  <p className="serif italic">say something sweet...</p>
                </div>
              )}
              {messages.map((m, i) => {
                const isMine = m.sender === identity;
                const prev = messages[i - 1];
                const showDay = !prev || !sameDay(prev.created_at, m.created_at);
                return (
                  <div key={m.id}>
                    {showDay && (
                      <div className="flex justify-center my-3">
                        <span className="text-[10px] uppercase tracking-widest bg-white/70 text-blush-400 px-3 py-1 rounded-full">
                          {dayLabel(m.created_at)}
                        </span>
                      </div>
                    )}
                    <div className={`flex ${isMine ? "justify-end" : "justify-start"}`}>
                      <div
                        className={`max-w-[75%] px-3 py-2 rounded-2xl text-sm leading-snug shadow-sm ${
                          isMine
                            ? "bg-gradient-to-br from-blush-300 to-peach-300 text-white rounded-br-sm"
                            : "bg-white text-[#4a2e3a] rounded-bl-sm border border-blush-100"
                        }`}
                      >
                        <div className="whitespace-pre-wrap break-words">{m.content}</div>
                        <div
                          className={`text-[10px] mt-1 text-right ${
                            isMine ? "text-white/80" : "text-blush-300"
                          }`}
                        >
                          {formatTime(m.created_at)}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Composer */}
            {sendError && (
              <div className="px-3 py-1.5 text-xs text-rose-600 bg-rose-50 border-t border-rose-100 text-center">
                {sendError}
              </div>
            )}
            <form
              onSubmit={handleSend}
              className="flex items-end gap-2 p-3 bg-white border-t border-blush-100"
            >
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSend(e as any);
                  }
                }}
                rows={1}
                placeholder="type a little love note..."
                className="flex-1 resize-none max-h-32 px-4 py-2 rounded-2xl bg-blush-50 border border-blush-100 focus:outline-none focus:border-blush-300 text-sm"
              />
              <button
                type="submit"
                disabled={!text.trim() || sending}
                className="w-11 h-11 shrink-0 rounded-full bg-gradient-to-br from-blush-300 to-peach-300 text-white shadow-md flex items-center justify-center disabled:opacity-50"
                aria-label="send"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M3 20l18-8L3 4v6l13 2-13 2v6z"
                    fill="currentColor"
                  />
                </svg>
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}
