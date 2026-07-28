-- Run this once in the Supabase SQL editor after creating your project.
-- Safe to re-run; uses IF NOT EXISTS everywhere.

create table if not exists public.messages (
  id uuid primary key default gen_random_uuid(),
  sender text not null check (sender in ('diya','me')),
  content text not null,
  created_at timestamptz not null default now()
);

create index if not exists messages_created_at_idx
  on public.messages (created_at);

alter table public.messages enable row level security;

-- Web Push subscriptions (one row per device per identity)
create table if not exists public.push_subscriptions (
  id uuid primary key default gen_random_uuid(),
  identity text not null check (identity in ('diya','me')),
  endpoint text not null unique,
  p256dh text not null,
  auth text not null,
  user_agent text,
  created_at timestamptz not null default now()
);

create index if not exists push_subscriptions_identity_idx
  on public.push_subscriptions (identity);

alter table public.push_subscriptions enable row level security;

-- Grants (needed because "Auto-expose new tables" was disabled at project setup)
grant all on public.messages to service_role, anon, authenticated;
grant all on public.push_subscriptions to service_role, anon, authenticated;
grant usage on schema public to service_role, anon, authenticated;
