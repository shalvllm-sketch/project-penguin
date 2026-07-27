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
      } catch {
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
      } catch { /* transient */ }
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

    const tempId = "temp-" + Math.random().toString(36).slice(2);
    const optimistic: Msg = { id: tempId, sender: identity!, content, created_at: new Date().toISOString() };
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
      setMessages((prev) => prev.map((m) => (m.id === tempId ? j.message : m)));
      lastFetchRef.current = j.message.created_at;
    } catch (err: any) {
      setMessages((prev) => prev.filter((m) => m.id !== tempId));
      setText(content);
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
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-ink/40 backdrop-blur-sm p-0 sm:p-6 fade-up">
      <div className="w-full sm:max-w-md h-[92vh] sm:h-[620px] bg-paper shadow-lift overflow-hidden flex flex-col border border-ink/10">
        {/* Header */}
        <div className="px-5 py-4 flex items-center gap-3 border-b border-ink/10 bg-ivory">
          <div className="w-9 h-9 rounded-full bg-rose text-ivory flex items-center justify-center serif text-lg leading-none">
            {identity === "diya" ? "D" : identity === "me" ? "M" : "◦"}
          </div>
          <div className="flex-1 min-w-0">
            <div className="serif text-lg text-ink leading-none">correspondence</div>
            <div className="text-[10px] tracking-widest2 uppercase text-ink-soft mt-1.5">
              {identity ? (identity === "diya" ? "signed as Diya" : "signed as you") : "private"}
            </div>
          </div>
          {identity && (
            <button
              onClick={handleLogout}
              className="text-[10px] tracking-widest2 uppercase text-ink-soft hover:text-ink"
              aria-label="log out"
            >
              log out
            </button>
          )}
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full hover:bg-ink/5 flex items-center justify-center text-ink text-lg"
            aria-label="close chat"
          >
            ×
          </button>
        </div>

        {needsAuth ? (
          <form onSubmit={handleAuth} className="flex-1 flex flex-col items-center justify-center gap-5 p-8 bg-paper">
            <span className="eyebrow">private · two persons only</span>
            <p className="serif italic text-2xl text-ink text-center leading-snug max-w-xs">
              tell me the secret word.
            </p>
            <input
              type="password"
              autoFocus
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="…"
              className="w-full max-w-xs px-1 py-2 bg-transparent border-b border-ink/25 focus:outline-none focus:border-ink text-center serif text-lg text-ink placeholder:text-ink-mute"
            />
            {authError && <p className="text-xs text-rose-deep">{authError}</p>}
            <button
              type="submit"
              disabled={authing || !password}
              className="mt-2 px-6 py-2 border border-ink text-ink text-xs tracking-widest2 uppercase hover:bg-ink hover:text-ivory transition disabled:opacity-40"
            >
              {authing ? "opening…" : "enter"}
            </button>
          </form>
        ) : (
          <>
            <div ref={scrollRef} className="chat-scroll flex-1 overflow-y-auto px-5 py-6 bg-paper space-y-2">
              {loadError && (
                <p className="text-center text-xs text-rose-deep">{loadError}</p>
              )}
              {messages.length === 0 && !loadError && (
                <div className="h-full flex flex-col items-center justify-center text-ink-soft gap-2">
                  <span className="ornament text-3xl">&mdash;</span>
                  <p className="serif italic text-lg">say something sweet.</p>
                </div>
              )}
              {messages.map((m, i) => {
                const isMine = m.sender === identity;
                const prev = messages[i - 1];
                const showDay = !prev || !sameDay(prev.created_at, m.created_at);
                return (
                  <div key={m.id}>
                    {showDay && (
                      <div className="flex items-center gap-3 my-5">
                        <span className="flex-1 h-px bg-ink/10" />
                        <span className="text-[10px] tracking-widest2 uppercase text-ink-mute">
                          {dayLabel(m.created_at)}
                        </span>
                        <span className="flex-1 h-px bg-ink/10" />
                      </div>
                    )}
                    <div className={`flex ${isMine ? "justify-end" : "justify-start"}`}>
                      <div
                        className={`max-w-[78%] px-3.5 py-2.5 text-[15px] leading-snug serif ${
                          isMine
                            ? "bg-ink text-ivory rounded-[16px] rounded-br-[4px]"
                            : "bg-ivory text-ink border border-ink/10 rounded-[16px] rounded-bl-[4px]"
                        }`}
                      >
                        <div className="whitespace-pre-wrap break-words">{m.content}</div>
                        <div
                          className={`text-[10px] mt-1 text-right tracking-wider2 uppercase ${
                            isMine ? "text-ivory/60" : "text-ink-mute"
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

            {sendError && (
              <div className="px-4 py-2 text-[10px] tracking-widest2 uppercase text-rose-deep bg-rose-wash/40 border-t border-rose/20 text-center">
                {sendError}
              </div>
            )}
            <form onSubmit={handleSend} className="flex items-end gap-3 px-4 py-3 bg-ivory border-t border-ink/10">
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
                placeholder="write a little love note…"
                className="flex-1 resize-none max-h-32 px-2 py-2 bg-transparent border-b border-ink/15 focus:outline-none focus:border-ink text-[15px] serif placeholder:text-ink-mute placeholder:italic"
              />
              <button
                type="submit"
                disabled={!text.trim() || sending}
                className="shrink-0 px-4 py-2 border border-ink text-ink text-[10px] tracking-widest2 uppercase hover:bg-ink hover:text-ivory transition disabled:opacity-30"
                aria-label="send"
              >
                send
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}
