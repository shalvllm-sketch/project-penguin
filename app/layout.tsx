import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "For Diya 💌",
  description: "A little corner of the internet, just for us.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
