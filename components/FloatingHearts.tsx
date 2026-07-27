"use client";

import { useEffect, useState } from "react";

const HEARTS = ["💕", "💖", "🌸", "💗", "🩷", "✨", "🌷"];

type Heart = {
  left: number;
  delay: number;
  duration: number;
  size: number;
  emoji: string;
};

export default function FloatingHearts({ count = 18 }: { count?: number }) {
  const [items, setItems] = useState<Heart[]>([]);

  useEffect(() => {
    setItems(
      Array.from({ length: count }).map((_, i) => ({
        left: Math.random() * 100,
        delay: Math.random() * 8,
        duration: 8 + Math.random() * 10,
        size: 14 + Math.random() * 22,
        emoji: HEARTS[i % HEARTS.length],
      }))
    );
  }, [count]);

  return (
    <div className="pointer-events-none fixed inset-0 overflow-hidden z-0">
      {items.map((h, i) => (
        <span
          key={i}
          className="absolute animate-float select-none"
          style={{
            left: `${h.left}%`,
            fontSize: `${h.size}px`,
            animationDelay: `${h.delay}s`,
            animationDuration: `${h.duration}s`,
            filter: "drop-shadow(0 4px 10px rgba(255,157,188,0.35))",
          }}
        >
          {h.emoji}
        </span>
      ))}
    </div>
  );
}
