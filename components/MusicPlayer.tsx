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
    if (!query.trim()) {
      setResults([]);
      return;
    }
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
    return () => {
      controller.abort();
      clearTimeout(t);
    };
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
    // Give the <audio> element a beat to update its src
    setTimeout(async () => {
      try {
        await audioRef.current?.play();
      } catch {
        setPlaying(false);
      }
    }, 40);
  }

  function toggle() {
    const el = audioRef.current;
    if (!el || !current) return;
    if (el.paused) {
      el.play().then(() => setPlaying(true));
    } else {
      el.pause();
      setPlaying(false);
    }
  }

  return (
    <div className="w-full bg-white/70 backdrop-blur-md rounded-3xl border border-blush-100 shadow-sm p-6 sm:p-8 animate-fade-in">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blush-300 to-peach-300 flex items-center justify-center text-white text-lg shadow">
          🎵
        </div>
        <div>
          <h3 className="serif text-2xl text-blush-400 leading-none">our little jukebox</h3>
          <p className="text-xs text-peach-400 mt-1">search a song, i&apos;ll play it for you 💕</p>
        </div>
      </div>

      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. blinding lights, kesariya, taylor swift..."
          className="w-full px-4 py-3 pl-11 rounded-2xl bg-blush-50 border border-blush-100 focus:outline-none focus:border-blush-300 text-sm"
        />
        <span className="absolute left-4 top-1/2 -translate-y-1/2 text-blush-300">🔎</span>
        {loading && (
          <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-blush-300 animate-pulse">
            looking...
          </span>
        )}
      </div>

      {results.length > 0 && (
        <div className="mt-4 max-h-72 overflow-y-auto chat-scroll space-y-2">
          {results.map((t) => {
            const isPlayingThis = current?.trackId === t.trackId && playing;
            return (
              <button
                key={t.trackId}
                onClick={() => play(t)}
                className={`w-full flex items-center gap-3 p-2 rounded-2xl text-left transition ${
                  current?.trackId === t.trackId
                    ? "bg-blush-100"
                    : "bg-white hover:bg-blush-50"
                } border border-blush-100`}
              >
                <img
                  src={t.artworkUrl100}
                  alt=""
                  className="w-12 h-12 rounded-xl shadow-sm object-cover"
                />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-semibold text-[#4a2e3a] truncate">
                    {t.trackName}
                  </div>
                  <div className="text-xs text-peach-400 truncate">{t.artistName}</div>
                </div>
                <span className="text-blush-400 text-lg">
                  {isPlayingThis ? "❚❚" : "▶"}
                </span>
              </button>
            );
          })}
        </div>
      )}

      {current && (
        <div className="mt-5 p-4 rounded-2xl bg-gradient-to-br from-blush-100 to-peach-100 border border-blush-200 flex items-center gap-4 animate-pop-in">
          <div className={`relative ${playing ? "animate-spin-slow" : ""}`}>
            <img
              src={current.artworkUrl100}
              alt=""
              className="w-16 h-16 rounded-full shadow-md object-cover"
              style={playing ? { animation: "spin 6s linear infinite" } : undefined}
            />
            <div className="absolute inset-0 rounded-full bg-black/10 flex items-center justify-center">
              <div className="w-2 h-2 rounded-full bg-white/90" />
            </div>
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-semibold text-blush-400 truncate">
              {current.trackName}
            </div>
            <div className="text-xs text-peach-400 truncate">{current.artistName}</div>
            <div className="mt-2 h-1 rounded-full bg-white overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-blush-300 to-peach-300 transition-all"
                style={{ width: `${Math.min(100, progress * 100)}%` }}
              />
            </div>
            <div className="flex justify-between text-[10px] text-peach-400 mt-1">
              <span>30-sec preview</span>
              {current.trackViewUrl && (
                <a
                  href={current.trackViewUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="underline hover:text-blush-400"
                >
                  full song ↗
                </a>
              )}
            </div>
          </div>
          <button
            onClick={toggle}
            className="w-11 h-11 shrink-0 rounded-full bg-gradient-to-br from-blush-300 to-peach-300 text-white shadow-md flex items-center justify-center text-lg"
            aria-label={playing ? "pause" : "play"}
          >
            {playing ? "❚❚" : "▶"}
          </button>
          <audio ref={audioRef} src={current.previewUrl} preload="auto" />
        </div>
      )}

      {!current && !loading && results.length === 0 && query.trim() && (
        <p className="mt-4 text-center text-sm text-peach-400 italic">
          no matches — try another song?
        </p>
      )}
      {!current && !query.trim() && (
        <p className="mt-4 text-center text-xs text-blush-300 italic">
          suggest: pasoori · kesariya · blinding lights · agar tum saath ho
        </p>
      )}
    </div>
  );
}
