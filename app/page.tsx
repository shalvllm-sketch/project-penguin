"use client";

import { useState } from "react";
import FloatingHearts from "@/components/FloatingHearts";
import TogetherCounter from "@/components/TogetherCounter";
import ChatPanel from "@/components/ChatPanel";

export default function Home() {
  const [chatOpen, setChatOpen] = useState(false);

  return (
    <main className="relative min-h-screen overflow-x-hidden">
      <FloatingHearts />

      <div className="relative z-10 max-w-2xl mx-auto px-6 py-16 sm:py-24 flex flex-col items-center gap-14">
        {/* Hero */}
        <section className="text-center flex flex-col items-center gap-4 animate-fade-in">
          <p className="text-blush-300 tracking-[0.4em] text-xs uppercase">for the one &amp; only</p>
          <h1 className="serif text-6xl sm:text-8xl font-medium text-blush-400 leading-none">
            Diya
          </h1>
          <p className="serif italic text-xl sm:text-2xl text-peach-400 max-w-md">
            a tiny corner of the internet, built just for you 💕
          </p>
        </section>

        {/* Counter */}
        <section className="w-full">
          <TogetherCounter />
        </section>

        {/* Sweet nothings */}
        <section className="bg-white/70 backdrop-blur-md rounded-3xl border border-blush-100 shadow-sm p-8 sm:p-10 text-center serif animate-fade-in">
          <p className="text-2xl sm:text-3xl leading-relaxed text-blush-400 italic">
            &ldquo;of all the ordinary miracles in my life,<br />
            you&apos;re easily my favourite one.&rdquo;
          </p>
          <div className="mt-6 flex justify-center gap-4 text-2xl">
            <span>🌸</span><span>💗</span><span>🌷</span>
          </div>
          <p className="mt-6 text-sm text-peach-400 not-italic">
            you make every regular tuesday feel like something worth remembering.
            thank you for being the softest, silliest, safest part of my day.
            i love you loudly. i love you quietly. i love you always.
          </p>
        </section>

        {/* Little "about us" grid */}
        <section className="w-full grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            { emoji: "💌", title: "our day", body: "7 sept 2024 — the day everything got softer." },
            { emoji: "🎂", title: "diya's day", body: "9 jan — the world got its best gift." },
            { emoji: "🎉", title: "my day", body: "9 may — the day you got stuck with me 😉" },
          ].map((c) => (
            <div
              key={c.title}
              className="bg-white/70 backdrop-blur-md rounded-2xl border border-blush-100 p-5 text-center shadow-sm hover:shadow-md hover:-translate-y-0.5 transition"
            >
              <div className="text-3xl">{c.emoji}</div>
              <div className="serif text-lg text-blush-400 mt-2">{c.title}</div>
              <p className="text-xs text-peach-400 mt-1 leading-relaxed">{c.body}</p>
            </div>
          ))}
        </section>

        {/* Footer */}
        <footer className="text-center text-xs text-blush-300 pt-6">
          made with 🩷 · just for us
        </footer>
      </div>

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
