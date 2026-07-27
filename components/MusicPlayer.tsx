"use client";

import { useEffect, useRef, useState } from "react";

type Track = {
  trackId: number;
  trackName: string;
  artistName: string;
  collectionName?: string;
  artworkUrl100: string;
  previewUrl: string;
  trackViewUrl?: string;
};

export default function MusicPlayer() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Track[]>([]);
  const [loading, setLoading] = useState(false);
  const [current, setCurrent] = useState<Track | null>(null);
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (!query.trim()) { setResults([]); return; }
    setLoading(true);
    const controller = new AbortController();
    const t = setTimeout(async () => {
      try {
        const r = await fetch(
          `https://itunes.apple.com/search?term=${encodeURIComponent(query)}&entity=song&limit=8`,
          { signal: controller.signal }
        );
        const j = await r.json();
        setResults(
          (j.results ?? []).filter((x: Track) => x.previewUrl).map((x: Track) => ({
            ...x,
            artworkUrl100: x.artworkUrl100?.replace("100x100", "300x300"),
          }))
        );
      } catch (e: any) {
        if (e?.name !== "AbortError") setResults([]);
      } finally {
        setLoading(false);
      }
    }, 350);
    return () => { controller.abort(); clearTimeout(t); };
  }, [query]);

  useEffect(() => {
    const el = audioRef.current;
    if (!el) return;
    const onTime = () => setProgress(el.currentTime / (el.duration || 30));
    const onEnd = () => { setPlaying(false); setProgress(0); };
    el.addEventListener("timeupdate", onTime);
    el.addEventListener("ended", onEnd);
    return () => {
      el.removeEventListener("timeupdate", onTime);
      el.removeEventListener("ended", onEnd);
    };
  }, [current]);

  async function play(t: Track) {
    setCurrent(t);
    setPlaying(true);
    setProgress(0);
    setTimeout(async () => {
      try { await audioRef.current?.play(); }
      catch { setPlaying(false); }
    }, 40);
  }

  function toggle() {
    const el = audioRef.current;
    if (!el || !current) return;
    if (el.paused) el.play().then(() => setPlaying(true));
    else { el.pause(); setPlaying(false); }
  }

  return (
    <div className="fade-up">
      <div className="flex items-center gap-4 mb-6">
        <span className="rule-w-32" />
        <span className="eyebrow">Chapter III &middot; a song for you</span>
      </div>
      <h2 className="serif text-3xl sm:text-4xl font-light text-ink leading-tight max-w-xl">
        Search anything. I&apos;ll play it for you —
        <span className="italic text-rose"> the way you like it, slow.</span>
      </h2>

      <div className="mt-8 relative max-w-xl">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="pasoori, taylor swift, kesariya…"
          className="w-full px-5 py-4 pr-24 rounded-none bg-transparent border-b border-ink/20 focus:outline-none focus:border-ink text-lg serif placeholder:text-ink-mute placeholder:italic"
        />
        <div className="absolute right-0 top-1/2 -translate-y-1/2 text-xs eyebrow text-ink-soft">
          {loading ? "listening…" : "search"}
        </div>
      </div>

      {results.length > 0 && (
        <div className="mt-6 max-w-xl divide-y divide-ink/10 border-t border-b border-ink/10">
          {results.map((t) => {
            const isPlayingThis = current?.trackId === t.trackId && playing;
            return (
              <button
                key={t.trackId}
                onClick={() => play(t)}
                className={`w-full flex items-center gap-4 py-3 px-1 text-left transition ${
                  current?.trackId === t.trackId ? "bg-rose-wash/40" : "hover:bg-rose-wash/20"
                }`}
              >
                <img
                  src={t.artworkUrl100}
                  alt=""
                  className="w-12 h-12 object-cover shadow-soft"
                />
                <div className="flex-1 min-w-0">
                  <div className="serif text-lg text-ink truncate leading-tight">
                    {t.trackName}
                  </div>
                  <div className="text-xs tracking-wider2 uppercase text-ink-soft truncate mt-1">
                    {t.artistName}
                  </div>
                </div>
                <span className="text-rose text-lg font-light">
                  {isPlayingThis ? "❚❚" : "▷"}
                </span>
              </button>
            );
          })}
        </div>
      )}

      {current && (
        <div className="mt-8 max-w-xl border-t border-b border-ink/15 py-6 flex items-center gap-5">
          <img
            src={current.artworkUrl100}
            alt=""
            className="w-20 h-20 object-cover shadow-soft"
            style={playing ? { animation: "spin 12s linear infinite", borderRadius: "9999px" } : undefined}
          />
          <div className="flex-1 min-w-0">
            <div className="serif text-xl text-ink truncate leading-tight">{current.trackName}</div>
            <div className="text-xs tracking-wider2 uppercase text-ink-soft truncate mt-1">
              {current.artistName}
            </div>
            <div className="mt-3 h-px bg-ink/15 overflow-hidden">
              <div className="h-full bg-rose transition-all" style={{ width: `${Math.min(100, progress * 100)}%` }} />
            </div>
            <div className="flex justify-between text-[10px] tracking-wider2 uppercase text-ink-soft mt-2">
              <span>a thirty-second preview</span>
              {current.trackViewUrl && (
                <a href={current.trackViewUrl} target="_blank" rel="noreferrer" className="underline underline-offset-2 hover:text-ink">
                  full song ↗
                </a>
              )}
            </div>
          </div>
          <button
            onClick={toggle}
            className="w-12 h-12 shrink-0 rounded-full border border-ink text-ink flex items-center justify-center hover:bg-ink hover:text-ivory transition"
            aria-label={playing ? "pause" : "play"}
          >
            {playing ? "❚❚" : "▷"}
          </button>
          <audio ref={audioRef} src={current.previewUrl} preload="auto" />
        </div>
      )}

      {!current && !loading && results.length === 0 && query.trim() && (
        <p className="mt-6 text-sm text-ink-soft italic">nothing found — try another?</p>
      )}
      {!current && !query.trim() && (
        <p className="mt-6 text-xs tracking-wider2 uppercase text-ink-mute">
          try &nbsp;&middot;&nbsp; pasoori &nbsp;&middot;&nbsp; kesariya &nbsp;&middot;&nbsp; blinding lights &nbsp;&middot;&nbsp; agar tum saath ho
        </p>
      )}
    </div>
  );
}
