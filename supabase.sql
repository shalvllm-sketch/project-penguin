-- Run this once in the Supabase SQL editor after creating your project.

create table if not exists public.messages (
  id uuid primary key default gen_random_uuid(),
  sender text not null check (sender in ('diya','me')),
  content text not null,
  created_at timestamptz not null default now()
);

create index if not exists messages_created_at_idx
  on public.messages (created_at);

-- Enable RLS. We only ever read/write via the service_role key from
-- our Next.js API routes, so no public policies are needed.
alter table public.messages enable row level security;
