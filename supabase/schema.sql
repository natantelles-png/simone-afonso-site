-- Simone Afonso: banco do blog (Supabase)
-- Como usar: Supabase > SQL Editor > New query > colar tudo > Run.

create extension if not exists pgcrypto;

create table if not exists public.posts (
  id          uuid primary key default gen_random_uuid(),
  slug        text unique not null check (slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$'),
  title       text not null,
  category    text not null default 'Neuroarquitetura',
  excerpt     text not null default '',      -- resumo curto, vira a descrição no Google
  answer      text not null default '',      -- resposta direta (AEO): 40 a 60 palavras
  body_html   text not null default '',
  cover_url   text,
  cover_alt   text not null default '',
  keywords    text not null default '',
  faq         jsonb not null default '[]'::jsonb,   -- [{"q":"...","a":"..."}]
  status      text not null default 'draft' check (status in ('draft','published')),
  publish_at  timestamptz not null default now(),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

create index if not exists posts_publish_idx on public.posts (status, publish_at desc);

create or replace function public.posts_touch() returns trigger
language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end $$;

drop trigger if exists posts_touch on public.posts;
create trigger posts_touch before update on public.posts
for each row execute function public.posts_touch();

-- Segurança por linha: o público só lê posts publicados; só quem fez login escreve.
alter table public.posts enable row level security;

drop policy if exists "leitura publica" on public.posts;
create policy "leitura publica" on public.posts
  for select to anon
  using (status = 'published' and publish_at <= now());

drop policy if exists "autora le tudo" on public.posts;
create policy "autora le tudo" on public.posts
  for select to authenticated using (true);

drop policy if exists "autora escreve" on public.posts;
create policy "autora escreve" on public.posts
  for insert to authenticated with check (true);

drop policy if exists "autora edita" on public.posts;
create policy "autora edita" on public.posts
  for update to authenticated using (true) with check (true);

drop policy if exists "autora apaga" on public.posts;
create policy "autora apaga" on public.posts
  for delete to authenticated using (true);

-- Imagens do blog: leitura pública, escrita só com login.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('blog-images', 'blog-images', true, 5242880, array['image/jpeg','image/png','image/webp'])
on conflict (id) do update set public = true, file_size_limit = 5242880,
  allowed_mime_types = array['image/jpeg','image/png','image/webp'];

drop policy if exists "imagens leitura" on storage.objects;
create policy "imagens leitura" on storage.objects
  for select to anon, authenticated using (bucket_id = 'blog-images');

drop policy if exists "imagens envio" on storage.objects;
create policy "imagens envio" on storage.objects
  for insert to authenticated with check (bucket_id = 'blog-images');

drop policy if exists "imagens troca" on storage.objects;
create policy "imagens troca" on storage.objects
  for update to authenticated using (bucket_id = 'blog-images');

drop policy if exists "imagens apagar" on storage.objects;
create policy "imagens apagar" on storage.objects
  for delete to authenticated using (bucket_id = 'blog-images');
