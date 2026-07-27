"use client";

import { useEffect, useState } from "react";

type Mote = {
  left: number;
  delay: number;
  duration: number;
  size: number;
  opacity: number;
};

// Slow-drifting dust motes — a quiet, editorial texture, not confetti.
export default function FloatingHearts({ count = 22 }: { count?: number }) {
  const [items, setItems] = useState<Mote[]>([]);

  useEffect(() => {
    setItems(
      Array.from({ length: count }).map(() => ({
        left: Math.random() * 100,
        delay: Math.random() * 22,
        duration: 22 + Math.random() * 28,
        size: 2 + Math.random() * 4,
        opacity: 0.25 + Math.random() * 0.35,
      }))
    );
  }, [count]);

  return (
    <div className="pointer-events-none fixed inset-0 overflow-hidden z-0">
      {items.map((m, i) => (
        <span
          key={i}
          className="absolute rounded-full"
          style={{
            left: `${m.left}%`,
            bottom: 0,
            width: `${m.size}px`,
            height: `${m.size}px`,
            background: "radial-gradient(circle, rgba(168,95,118,0.9), rgba(168,95,118,0) 70%)",
            animation: `drift ${m.duration}s linear ${m.delay}s infinite`,
            opacity: m.opacity,
          }}
        />
      ))}
    </div>
  );
}
