"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import FloatingHearts from "@/components/FloatingHearts";
import TogetherCounter from "@/components/TogetherCounter";
import ChatPanel from "@/components/ChatPanel";
import MusicPlayer from "@/components/MusicPlayer";

// Client-only so it never prerenders (three.js touches window at import time)
const Heart3D = dynamic(() => import("@/components/Heart3D"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center text-6xl animate-pulse">💗</div>
  ),
});

export default function Home() {
  const [chatOpen, setChatOpen] = useState(false);

  return (
    <main className="relative min-h-screen overflow-x-hidden">
      <FloatingHearts />

      {/* ─── HERO ─────────────────────────────────────────── */}
      <section className="relative z-10 min-h-screen flex flex-col lg:flex-row items-center justify-center px-6 py-10 gap-6 lg:gap-4 max-w-6xl mx-auto">
        <div className="flex-1 flex flex-col items-center lg:items-start text-center lg:text-left animate-fade-in">
          <p className="text-blush-300 tracking-[0.4em] text-xs uppercase mb-3">
            for the one &amp; only
          </p>
          <h1 className="serif text-7xl sm:text-8xl lg:text-[9rem] font-medium text-blush-400 leading-none">
            Diya
          </h1>
          <p className="serif italic text-2xl lg:text-3xl text-peach-400 mt-4 max-w-md">
            a tiny corner of the internet,<br className="hidden sm:block" />
            built just for you 💕
          </p>
          <div className="mt-6 flex flex-wrap gap-2 justify-center lg:justify-start">
            <a
              href="#counter"
              className="px-5 py-2 rounded-full bg-white/70 backdrop-blur-sm border border-blush-100 text-sm text-blush-400 hover:bg-white transition"
            >
              our story ↓
            </a>
            <button
              onClick={() => setChatOpen(true)}
              className="px-5 py-2 rounded-full bg-gradient-to-r from-blush-300 to-peach-300 text-white text-sm font-semibold shadow-md hover:shadow-lg transition"
            >
              💌 whisper to me
            </button>
          </div>
        </div>

        <div className="flex-1 w-full h-[300px] sm:h-[420px] lg:h-[500px] relative">
          <Heart3D />
        </div>

        {/* scroll indicator */}
        <div className="hidden lg:block absolute bottom-6 left-1/2 -translate-x-1/2 text-blush-300 text-xs tracking-widest uppercase animate-bounce">
          scroll ↓
        </div>
      </section>

      {/* ─── COUNTER ──────────────────────────────────────── */}
      <section id="counter" className="relative z-10 max-w-3xl mx-auto px-6 py-16">
        <TogetherCounter />
      </section>

      {/* ─── SWEET NOTHINGS ──────────────────────────────── */}
      <section className="relative z-10 max-w-2xl mx-auto px-6 py-10">
        <div className="bg-white/70 backdrop-blur-md rounded-3xl border border-blush-100 shadow-sm p-8 sm:p-12 text-center serif animate-fade-in">
          <div className="flex justify-center mb-4 text-3xl">🌸 💗 🌷</div>
          <p className="text-2xl sm:text-3xl leading-relaxed text-blush-400 italic">
            &ldquo;of all the ordinary miracles in my life,<br />
            you&apos;re easily my favourite one.&rdquo;
          </p>
          <p className="mt-6 text-sm text-peach-400 not-italic leading-relaxed">
            you make every regular tuesday feel like something worth remembering.
            thank you for being the softest, silliest, safest part of my day.
            i love you loudly. i love you quietly. i love you always.
          </p>
        </div>
      </section>

      {/* ─── MUSIC PLAYER ────────────────────────────────── */}
      <section className="relative z-10 max-w-2xl mx-auto px-6 py-10">
        <MusicPlayer />
      </section>

      {/* ─── DATE CARDS ──────────────────────────────────── */}
      <section className="relative z-10 max-w-4xl mx-auto px-6 py-10">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            { emoji: "💌", title: "our day", body: "7 sept 2024 — the day everything got softer." },
            { emoji: "🎂", title: "diya's day", body: "9 jan — the world got its best gift." },
            { emoji: "🎉", title: "my day", body: "9 may — the day you got stuck with me 😉" },
          ].map((c) => (
            <div
              key={c.title}
              className="bg-white/70 backdrop-blur-md rounded-2xl border border-blush-100 p-6 text-center shadow-sm hover:shadow-lg hover:-translate-y-1 hover:rotate-[-1deg] transition-all duration-300"
            >
              <div className="text-4xl mb-2">{c.emoji}</div>
              <div className="serif text-xl text-blush-400">{c.title}</div>
              <p className="text-xs text-peach-400 mt-2 leading-relaxed">{c.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ─── FOOTER ──────────────────────────────────────── */}
      <footer className="relative z-10 text-center text-xs text-blush-300 py-10">
        made with 🩷 · just for us
      </footer>

      {/* Floating chat button */}
      <button
        onClick={() => setChatOpen(true)}
        className="fixed bottom-6 right-6 z-40 group flex items-center gap-2 pl-4 pr-5 py-3 rounded-full bg-gradient-to-r from-blush-300 to-peach-300 text-white font-semibold shadow-xl hover:shadow-2xl hover:scale-105 transition"
        aria-label="open chat"
      >
        <span className="text-xl">💌</span>
        <span className="hidden sm:inline">our chat</span>
      </button>

      {chatOpen && <ChatPanel onClose={() => setChatOpen(false)} />}
    </main>
  );
}
