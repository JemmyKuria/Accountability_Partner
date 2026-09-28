-- ============================================================
-- Accountability Partner App — Supabase Schema
-- Uses Supabase's built-in auth.users for authentication.
-- All app tables reference auth.users(id) directly — no
-- separate "users" table needed unless extra profile fields
-- are wanted later.
-- ============================================================

-- Enable UUID generation (usually already on in Supabase)
create extension if not exists "uuid-ossp";

-- ------------------------------------------------------------
-- Table: goals
-- ------------------------------------------------------------
create table goals (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid not null references auth.users(id) on delete cascade,
    title text not null,
    deadline date,
    tag text,
    total_sessions_target integer not null default 1,
    current_sessions integer not null default 0,
    progress_manual float,
    pinned boolean not null default false,
    created_at timestamptz not null default now()
);
alter table goals add column if not exists goal_type text default 'Personal';
alter table goals add column if not exists priority text default 'Medium';
alter table goals add column if not exists description text;

-- ------------------------------------------------------------
-- Table: tasks
-- ------------------------------------------------------------
create table tasks (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid not null references auth.users(id) on delete cascade,
    title text not null,
    tag text,
    type text not null check (type in ('non_negotiable', 'bonus')),
    completed boolean not null default false,
    date date not null default current_date,
    created_at timestamptz not null default now()
);

-- ------------------------------------------------------------
-- Table: gratitude_entries
-- ------------------------------------------------------------
create table gratitude_entries (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid not null references auth.users(id) on delete cascade,
    content text not null,
    entry_date date not null default current_date,
    created_at timestamptz not null default now()
);
alter table gratitude_entries add column if not exists type text default 'Personal';

-- ------------------------------------------------------------
-- Table: sessions (detailed goal-progress logging)
-- ------------------------------------------------------------
create table sessions (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid not null references auth.users(id) on delete cascade,
    goal_id uuid not null references goals(id) on delete cascade,
    logged_at timestamptz not null default now()
);

-- ------------------------------------------------------------
-- Table: streaks (tracks current streak per user)
-- ------------------------------------------------------------
create table streaks (
    user_id uuid primary key references auth.users(id) on delete cascade,
    current_streak integer not null default 0,
    last_completed_date date
);

-- ------------------------------------------------------------
-- Useful indexes
-- ------------------------------------------------------------
create index idx_tasks_user_date on tasks(user_id, date);
create index idx_goals_user on goals(user_id);
create index idx_gratitude_user_date on gratitude_entries(user_id, entry_date);
create index idx_sessions_goal on sessions(goal_id);

-- ============================================================
-- Row Level Security — every user sees only their own data
-- ============================================================
alter table goals enable row level security;
alter table tasks enable row level security;
alter table gratitude_entries enable row level security;
alter table sessions enable row level security;
alter table streaks enable row level security;

-- goals policies
create policy "Users manage their own goals"
    on goals for all
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

-- tasks policies
create policy "Users manage their own tasks"
    on tasks for all
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

-- gratitude_entries policies
create policy "Users manage their own gratitude entries"
    on gratitude_entries for all
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

-- sessions policies
create policy "Users manage their own sessions"
    on sessions for all
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

-- streaks policies
create policy "Users manage their own streak"
    on streaks for all
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

create table profiles (
    user_id uuid primary key references auth.users(id) on delete cascade,
    cv_text text,
    cv_filename text,
    updated_at timestamptz not null default now()
);

-- ------------------------------------------------------------
-- Table: job_applications
-- One row per application the user is tracking.
-- unique(user_id, job_url) prevents duplicate entries.
-- ------------------------------------------------------------
create table job_applications (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid not null references auth.users(id) on delete cascade,
    job_url text not null,
    company text,
    position text,
    platform text,
    date_applied date not null default current_date,
    status text not null default 'Applied'
        check (status in (
            'Applied',
            'Under Review',
            'Interview Scheduled',
            'Interview Completed',
            'Rejected',
            'Offer',
            'No Response / Ghosted'
        )),
    notes text,
    created_at timestamptz not null default now(),
    unique (user_id, job_url)
);

-- ------------------------------------------------------------
-- Table: dismissed_jobs
-- Jobs the user has hidden from search results.
-- ------------------------------------------------------------
create table dismissed_jobs (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid not null references auth.users(id) on delete cascade,
    job_url text not null,
    dismissed_at timestamptz not null default now(),
    unique (user_id, job_url)
);

-- ------------------------------------------------------------
-- Indexes
-- ------------------------------------------------------------
create index idx_job_apps_user on job_applications(user_id, date_applied desc);
create index idx_job_apps_status on job_applications(user_id, status);
create index idx_dismissed_user on dismissed_jobs(user_id);

-- ------------------------------------------------------------
-- Row Level Security
-- ------------------------------------------------------------
alter table profiles enable row level security;
alter table job_applications enable row level security;
alter table dismissed_jobs enable row level security;

-- profiles: each user only sees / edits their own row
create policy "Users manage their own profile"
    on profiles for all
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

-- job_applications: each user only sees their own applications
create policy "Users manage their own job applications"
    on job_applications for all
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

-- dismissed_jobs: each user only sees their own dismissals
create policy "Users manage their own dismissed jobs"
    on dismissed_jobs for all
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);