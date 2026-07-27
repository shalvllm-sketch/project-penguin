"use client";

import { useEffect, useState } from "react";

const START = new Date("2024-09-07T00:00:00");

function diff(now: Date) {
  let years = now.getFullYear() - START.getFullYear();
  let months = now.getMonth() - START.getMonth();
  let days = now.getDate() - START.getDate();
  let hours = now.getHours() - START.getHours();
  let minutes = now.getMinutes() - START.getMinutes();
  let seconds = now.getSeconds() - START.getSeconds();

  if (seconds < 0) { seconds += 60; minutes -= 1; }
  if (minutes < 0) { minutes += 60; hours -= 1; }
  if (hours < 0) { hours += 24; days -= 1; }
  if (days < 0) {
    const prevMonth = new Date(now.getFullYear(), now.getMonth(), 0);
    days += prevMonth.getDate();
    months -= 1;
  }
  if (months < 0) { months += 12; years -= 1; }

  const totalDays = Math.floor((now.getTime() - START.getTime()) / 86400000);
  return { years, months, days, hours, minutes, seconds, totalDays };
}

export default function TogetherCounter() {
  const [now, setNow] = useState<Date | null>(null);

  useEffect(() => {
    setNow(new Date());
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  if (!now) {
    return (
      <div className="text-center text-blush-300/70 serif text-2xl">
        counting our forever...
      </div>
    );
  }

  const d = diff(now);
  const cell = "flex flex-col items-center px-3 sm:px-5 py-3 rounded-2xl bg-white/60 backdrop-blur-sm border border-blush-100 shadow-sm min-w-[64px]";

  return (
    <div className="flex flex-col items-center gap-4 animate-fade-in">
      <p className="serif italic text-blush-400 text-xl sm:text-2xl">
        together for
      </p>
      <div className="flex flex-wrap justify-center gap-2 sm:gap-3">
        {[
          ["years", d.years],
          ["months", d.months],
          ["days", d.days],
          ["hours", d.hours],
          ["mins", d.minutes],
          ["secs", d.seconds],
        ].map(([label, val]) => (
          <div key={label as string} className={cell}>
            <span className="serif text-3xl sm:text-4xl font-medium text-blush-400 tabular-nums">
              {String(val).padStart(2, "0")}
            </span>
            <span className="text-[10px] sm:text-xs uppercase tracking-widest text-peach-400/80 mt-1">
              {label}
            </span>
          </div>
        ))}
      </div>
      <p className="text-sm text-blush-300">
        that&apos;s <span className="font-semibold text-blush-400">{d.totalDays.toLocaleString()}</span> days of us 💕
      </p>
    </div>
  );
}
