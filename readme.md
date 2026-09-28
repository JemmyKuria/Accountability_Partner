# Accountability Partner — Setup

## 1. Create the Supabase project
1. Go to supabase.com and create a new project.
2. Open the SQL Editor and run `schema.sql` (included in this folder) to create
   all tables, indexes, and row-level security policies.
3. In Project Settings → API, copy your **Project URL** and **anon public key**.

## 2. Configure environment variables
Copy `.env.example` to `.env` and fill in the values from step 1:

```
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-anon-key
```

## 3. Install dependencies
```
pip install -r requirements.txt
```

## 4. Run the app
```
streamlit run app.py
```

## Project structure
```
accountability_app/
├── app.py                 # Entry point, auth gate, navigation
├── schema.sql              # Supabase table + RLS setup
├── db/
│   ├── supabase_client.py  # Client init + session attachment
│   └── queries.py          # All table reads/writes
├── logic/
│   └── business_logic.py   # Streak math, weekly score, tag-linking, sorting
└── views/
    ├── style.py             # Indigo & Coral CSS theme
    ├── auth_view.py          # Login / sign-up
    ├── daily_hub.py          # Gratitude, Non-Negotiables, Bonus tasks, streak
    ├── dashboard.py           # Goals dashboard
    └── gratitude_view.py      # Gratitude archive
```

## Notes
- Auth uses Supabase's built-in email/password sign-up — new accounts need to
  confirm their email before logging in (default Supabase behavior; can be
  turned off in Auth settings for faster testing).
- The streak logic resets if a day passes with the Non-Negotiables not all
  completed; see `logic/business_logic.py` for the exact rules.
- Deployment to Azure + Docker is intentionally **not** included yet — build
  and test locally first, then say the word when you're ready for that step.