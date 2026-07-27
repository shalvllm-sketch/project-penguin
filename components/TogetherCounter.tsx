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

  if (!now) return <div className="h-56" />;

  const d = diff(now);
  const units: Array<[string, number]> = [
    ["years", d.years],
    ["months", d.months],
    ["days", d.days],
    ["hours", d.hours],
    ["minutes", d.minutes],
    ["seconds", d.seconds],
  ];

  return (
    <div className="fade-up">
      <div className="flex items-center gap-4 mb-8">
        <span className="rule-w-32" />
        <span className="eyebrow">Chapter I &middot; the beginning</span>
      </div>
      <h2 className="serif text-4xl sm:text-5xl font-light text-ink leading-tight max-w-2xl">
        Seventh of September, twenty-twenty-four —
        <span className="italic text-rose"> the day everything got softer.</span>
      </h2>

      <div className="mt-10 grid grid-cols-3 sm:grid-cols-6 gap-x-4 gap-y-6 sm:gap-x-8 max-w-3xl">
        {units.map(([label, val]) => (
          <div key={label} className="flex flex-col">
            <span className="serif text-4xl sm:text-5xl font-light text-ink tabular-nums leading-none">
              {String(val).padStart(2, "0")}
            </span>
            <span className="mt-2 text-[10px] tracking-widest2 uppercase text-ink-soft">
              {label}
            </span>
          </div>
        ))}
      </div>

      <p className="mt-10 text-sm text-ink-soft max-w-md">
        <span className="ornament">&mdash;</span> that&apos;s{" "}
        <span className="text-ink font-medium">{d.totalDays.toLocaleString()}</span> days.
        each one a little quieter, a little sweeter, than the last.
      </p>
    </div>
  );
}
