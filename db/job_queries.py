"""
db/job_queries.py
-----------------
All Supabase queries for the Job Hunt feature. Every function accepts
the active supabase client as its first argument so that RLS (via the
user's session) is always enforced.

The UI layer should never call supabase directly — it goes through here.
"""

from datetime import date
from typing import Optional
import pandas as pd


# --------------------------------------------------------------------------
# CV Profile
# --------------------------------------------------------------------------

def save_cv_profile(client, user_id: str, cv_text: str, cv_filename: str) -> None:
    """Upsert the user's parsed CV. One row per user, always overwritten."""
    client.table("profiles").upsert(
        {
            "user_id": user_id,
            "cv_text": cv_text,
            "cv_filename": cv_filename,
            "updated_at": date.today().isoformat(),
        },
        on_conflict="user_id",
    ).execute()


def load_cv_profile(client, user_id: str) -> Optional[dict]:
    """Return {'cv_text': ..., 'cv_filename': ...} or None if not saved yet."""
    resp = (
        client.table("profiles")
        .select("cv_text, cv_filename")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    if resp.data:
        return resp.data[0]
    return None


# --------------------------------------------------------------------------
# Job Applications
# --------------------------------------------------------------------------

def add_application(
    client,
    user_id: str,
    job_url: str,
    company: str,
    position: str,
    platform: str,
    status: str = "Applied",
    notes: str = "",
) -> bool:
    """Insert a new application. Returns False if the URL already exists
    for this user (enforced by unique(user_id, job_url))."""
    try:
        client.table("job_applications").insert(
            {
                "user_id": user_id,
                "job_url": job_url,
                "company": company,
                "position": position,
                "platform": platform,
                "status": status,
                "notes": notes,
                "date_applied": date.today().isoformat(),
            }
        ).execute()
        return True
    except Exception:
        return False


def fetch_applications(client, user_id: str) -> pd.DataFrame:
    """Return all applications as a DataFrame, newest first."""
    resp = (
        client.table("job_applications")
        .select("*")
        .eq("user_id", user_id)
        .order("date_applied", desc=True)
        .execute()
    )
    if not resp.data:
        return pd.DataFrame(
            columns=[
                "id", "job_url", "company", "position", "platform",
                "date_applied", "status", "notes",
            ]
        )
    df = pd.DataFrame(resp.data)
    df["date_applied"] = pd.to_datetime(df["date_applied"]).dt.date
    return df


def update_application(client, app_id: str, status: str, notes: str) -> None:
    """Update status and notes on a single application."""
    client.table("job_applications").update(
        {"status": status, "notes": notes}
    ).eq("id", app_id).execute()


def delete_application(client, app_id: str) -> None:
    """Remove an application entirely."""
    client.table("job_applications").delete().eq("id", app_id).execute()


# --------------------------------------------------------------------------
# Dismissed Jobs (hidden from search results)
# --------------------------------------------------------------------------

def dismiss_job(client, user_id: str, job_url: str) -> None:
    """Mark a job as dismissed so it stops appearing in results."""
    try:
        client.table("dismissed_jobs").insert(
            {"user_id": user_id, "job_url": job_url}
        ).execute()
    except Exception:
        pass  # already dismissed — silently ignore


def fetch_dismissed(client, user_id: str) -> set:
    """Return the set of dismissed job URLs for this user."""
    resp = (
        client.table("dismissed_jobs")
        .select("job_url")
        .eq("user_id", user_id)
        .execute()
    )
    return {row["job_url"] for row in resp.data} if resp.data else set()


def clear_dismissed(client, user_id: str) -> None:
    """Wipe all dismissals for this user."""
    client.table("dismissed_jobs").delete().eq("user_id", user_id).execute()