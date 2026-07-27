"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import FloatingHearts from "@/components/FloatingHearts";
import TogetherCounter from "@/components/TogetherCounter";
import ChatPanel from "@/components/ChatPanel";
import MusicPlayer from "@/components/MusicPlayer";

const Heart3D = dynamic(() => import("@/components/Heart3D"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center text-ink-mute serif italic">rendering…</div>
  ),
});

export default function Home() {
  const [chatOpen, setChatOpen] = useState(false);

  return (
    <main className="relative min-h-screen overflow-x-hidden">
      <FloatingHearts />

      {/* Fixed top bar */}
      <header className="fixed top-0 inset-x-0 z-30 backdrop-blur-md bg-paper/60 border-b border-ink/10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="serif italic text-lg text-ink">for Diya</div>
          <div className="flex items-center gap-6">
            <a href="#chapter-i" className="eyebrow hidden sm:inline hover:text-ink">the beginning</a>
            <a href="#chapter-ii" className="eyebrow hidden sm:inline hover:text-ink">of you</a>
            <a href="#chapter-iii" className="eyebrow hidden sm:inline hover:text-ink">a song</a>
            <button
              onClick={() => setChatOpen(true)}
              className="text-[10px] tracking-widest2 uppercase text-ivory bg-ink px-4 py-2 hover:bg-rose-deep transition"
            >
              write
            </button>
          </div>
        </div>
      </header>

      {/* ─── HERO ─────────────────────────────────────── */}
      <section className="relative z-10 min-h-screen flex items-center px-6 pt-32 pb-16 max-w-6xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-4 items-center w-full">
          <div className="lg:col-span-7 order-2 lg:order-1">
            <div className="fade-up">
              <span className="eyebrow">a private letter, published quietly</span>
              <div className="mt-4 mb-4 flex items-baseline gap-4">
                <span className="rule-w-32" />
                <span className="serif italic text-ink-soft text-base">no. 001</span>
              </div>
            </div>
            <h1 className="serif fade-up-2 text-ink font-light leading-[0.9] text-[18vw] sm:text-[14vw] lg:text-[11rem]">
              Diya<span className="text-rose">.</span>
            </h1>
            <p className="serif italic text-2xl sm:text-3xl text-ink-soft mt-8 max-w-xl fade-up-3 leading-snug">
              — a tiny corner of the internet, kept just for you.
              some counting, a song or two, and a place for us to write.
            </p>
            <div className="mt-10 flex flex-wrap gap-3 fade-up-3">
              <a
                href="#chapter-i"
                className="px-5 py-3 text-[10px] tracking-widest2 uppercase border border-ink text-ink hover:bg-ink hover:text-ivory transition"
              >
                begin reading
              </a>
              <button
                onClick={() => setChatOpen(true)}
                className="px-5 py-3 text-[10px] tracking-widest2 uppercase bg-rose text-ivory hover:bg-rose-deep transition"
              >
                whisper to me
              </button>
            </div>
          </div>

          <div className="lg:col-span-5 order-1 lg:order-2 w-full h-[320px] sm:h-[440px] lg:h-[560px]">
            <Heart3D />
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-6"><div className="hairline" /></div>

      {/* ─── CHAPTER I · the counter ─────────────────── */}
      <section id="chapter-i" className="relative z-10 max-w-6xl mx-auto px-6 py-24 sm:py-32">
        <TogetherCounter />
      </section>

      <div className="max-w-6xl mx-auto px-6"><div className="hairline" /></div>

      {/* ─── CHAPTER II · sweet nothings ─────────────── */}
      <section id="chapter-ii" className="relative z-10 max-w-6xl mx-auto px-6 py-24 sm:py-32">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          <div className="lg:col-span-4">
            <div className="flex items-center gap-4 mb-6">
              <span className="rule-w-32" />
              <span className="eyebrow">Chapter II &middot; of you</span>
            </div>
            <h2 className="serif text-4xl sm:text-5xl font-light text-ink leading-tight">
              An ordinary
              <span className="italic text-rose"> miracle.</span>
            </h2>
          </div>

          <div className="lg:col-span-8">
            <p className="serif text-3xl sm:text-[2.4rem] italic text-ink leading-snug font-light">
              &ldquo;of all the ordinary miracles in my life,<br className="hidden sm:block" />
              you&apos;re easily my favourite one.&rdquo;
            </p>
            <p className="mt-8 text-base text-ink-soft leading-relaxed max-w-2xl">
              you make every regular tuesday feel like something worth remembering.
              thank you for being the softest, silliest, safest part of my day.
              i love you loudly. i love you quietly. i love you always.
            </p>

            <div className="mt-12 grid grid-cols-1 sm:grid-cols-3 gap-y-8 sm:gap-x-12 max-w-2xl">
              {[
                { label: "our day", date: "07 · 09 · 24", note: "the day everything got softer" },
                { label: "her day", date: "09 · 01", note: "the world got its best gift" },
                { label: "his day", date: "09 · 05", note: "the day she got stuck with him" },
              ].map((c) => (
                <div key={c.label} className="border-t border-ink/15 pt-4">
                  <div className="eyebrow">{c.label}</div>
                  <div className="serif text-2xl text-ink mt-2 tabular-nums">{c.date}</div>
                  <p className="text-xs text-ink-soft mt-2 italic">{c.note}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-6"><div className="hairline" /></div>

      {/* ─── CHAPTER III · music ─────────────────────── */}
      <section id="chapter-iii" className="relative z-10 max-w-6xl mx-auto px-6 py-24 sm:py-32">
        <MusicPlayer />
      </section>

      <div className="max-w-6xl mx-auto px-6"><div className="hairline" /></div>

      {/* ─── FOOTER ──────────────────────────────────── */}
      <footer className="relative z-10 max-w-6xl mx-auto px-6 py-16 flex flex-col sm:flex-row items-start sm:items-end justify-between gap-6">
        <div>
          <div className="serif italic text-xl text-ink">for Diya, always.</div>
          <p className="eyebrow mt-3">an edition of one &middot; est. 2024</p>
        </div>
        <div className="serif italic text-ink-mute text-sm">
          set in Fraunces &amp; Inter, on ivory paper.
        </div>
      </footer>

      {/* Floating chat button — subtle, inked */}
      <button
        onClick={() => setChatOpen(true)}
        className="fixed bottom-6 right-6 z-40 px-5 py-3 text-[10px] tracking-widest2 uppercase bg-ink text-ivory shadow-lift hover:bg-rose-deep transition"
        aria-label="open chat"
      >
        write to us
      </button>

      {chatOpen && <ChatPanel onClose={() => setChatOpen(false)} />}
    </main>
  );
}
