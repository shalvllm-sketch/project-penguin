# For Diya 💌

A soft little landing page + a private WhatsApp-style chat, just for the two of you.

- **Next.js 14 (App Router) + TypeScript + Tailwind**
- **Supabase** for storing chat messages
- **Vercel** for hosting
- Two passwords — one per person — server-side auth via httpOnly cookie. Your password decides your identity.
- Chat is polled every 2s for a realtime feel (simple, secure, works on Vercel serverless)

---

## 1. One-time setup

### a. Install deps

```bash
npm install
```

### b. Create a Supabase project

1. Go to https://supabase.com → New project (free tier is fine).
2. Once it's up, open **SQL editor** and paste the contents of `supabase.sql`. Run it.
3. Go to **Project Settings → API**. You'll need:
   - `Project URL` → `NEXT_PUBLIC_SUPABASE_URL`
   - `service_role` key (under "Project API Keys") → `SUPABASE_SERVICE_ROLE_KEY`
     - ⚠️ This key is a secret. Never commit it. We only use it server-side.

### c. Local env vars

Copy `.env.example` → `.env.local` and fill in the 3 values.

```bash
cp .env.example .env.local
```

### d. Run locally

```bash
npm run dev
```

Open http://localhost:3000. Click the 💌 button in the bottom-right. Your password decides who you are:
- `Pookie` → signs you in as **me**
- `Peanut` → signs Diya in as **Diya**

---

## 2. Deploy to Vercel

1. Create a **private** repo on GitHub and push:

   ```bash
   git init
   git add .
   git commit -m "initial commit — for diya 💕"
   git branch -M main
   git remote add origin git@github.com:<your-username>/<repo-name>.git
   git push -u origin main
   ```

2. Go to https://vercel.com → **Add new project** → import your repo.
3. Framework preset: **Next.js** (auto-detected). Don't touch build settings.
4. Under **Environment Variables**, add the same 4 vars from `.env.local`:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `PASSWORD_ME`
   - `PASSWORD_DIYA`
5. Deploy. Send Diya the URL 🎀

---

## 3. Customising

Everything is meant to be edited freely — poke around:

- Sweet words & birthdays: `app/page.tsx`
- Colours / fonts / animation speeds: `tailwind.config.ts`
- Chat vibe (bubbles, header, gate): `components/ChatPanel.tsx`
- "together for" start date: `components/TogetherCounter.tsx` (line 5)
- Passwords: change `PASSWORD_ME` / `PASSWORD_DIYA` in Vercel (and `.env.local`) — no code change needed

---

## Notes on the chat

- Anyone with the URL + password can open the chat. That's the whole security model. Change the password anytime.
- Messages live forever in the Supabase `messages` table until you delete them. You can browse / delete from the Supabase Table Editor.
- The Supabase `service_role` key is server-side only. It never reaches the browser.
- Polling every 2s means there's a tiny delay before messages appear. Good enough for love letters.

Have fun 🌷
