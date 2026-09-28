"""
All Supabase table reads/writes live here, kept separate from UI code.
Every function takes an already-authenticated `client` plus the
current `user_id`, and only ever touches that user's rows (RLS
enforces this server-side too, as a second line of defense).
"""
from datetime import date, timedelta


# ---------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------
def get_tasks_for_date(client, user_id, for_date: date, task_type: str = None):
    query = (
        client.table("tasks")
        .select("*")
        .eq("user_id", user_id)
        .eq("date", for_date.isoformat())
    )
    if task_type:
        query = query.eq("type", task_type)
    return query.execute().data


def add_task(client, user_id, title, task_type, tag=None, for_date: date = None):
    for_date = for_date or date.today()
    return (
        client.table("tasks")
        .insert(
            {
                "user_id": user_id,
                "title": title,
                "tag": tag,
                "type": task_type,
                "date": for_date.isoformat(),
            }
        )
        .execute()
        .data
    )


def set_task_completed(client, task_id, completed: bool):
    return (
        client.table("tasks")
        .update({"completed": completed})
        .eq("id", task_id)
        .execute()
        .data
    )


def get_weekly_bonus_count(client, user_id, week_start: date, week_end: date):
    result = (
        client.table("tasks")
        .select("id", count="exact")
        .eq("user_id", user_id)
        .eq("type", "bonus")
        .eq("completed", True)
        .gte("date", week_start.isoformat())
        .lte("date", week_end.isoformat())
        .execute()
    )
    return result.count or 0


# ---------------------------------------------------------------
# Streaks
# ---------------------------------------------------------------
def get_streak(client, user_id):
    result = (
        client.table("streaks").select("*").eq("user_id", user_id).execute().data
    )
    if result:
        return result[0]
    # No row yet — create one at zero.
    return (
        client.table("streaks")
        .insert({"user_id": user_id, "current_streak": 0, "last_completed_date": None})
        .execute()
        .data[0]
    )


def upsert_streak(client, user_id, current_streak: int, last_completed_date):
    return (
        client.table("streaks")
        .upsert(
            {
                "user_id": user_id,
                "current_streak": current_streak,
                "last_completed_date": last_completed_date.isoformat()
                if last_completed_date
                else None,
            }
        )
        .execute()
        .data
    )


# ---------------------------------------------------------------
# Goals
# ---------------------------------------------------------------
def get_goals(client, user_id):
    return client.table("goals").select("*").eq("user_id", user_id).execute().data


def add_goal(
    client, user_id, title, deadline, tag, total_sessions_target,
    goal_type="Personal", priority="Medium", description=None,
):
    return client.table("goals").insert({
        "user_id": user_id,
        "title": title,
        "deadline": deadline.isoformat() if deadline else None,
        "tag": tag,
        "total_sessions_target": total_sessions_target,
        "goal_type": goal_type,
        "priority": priority,
        "description": description,
    }).execute()


def update_goal_sessions(client, goal_id, current_sessions):
    return (
        client.table("goals")
        .update({"current_sessions": current_sessions})
        .eq("id", goal_id)
        .execute()
        .data
    )


def set_goal_manual_progress(client, goal_id, progress_manual: float):
    return (
        client.table("goals")
        .update({"progress_manual": progress_manual})
        .eq("id", goal_id)
        .execute()
        .data
    )


def set_goal_pinned(client, goal_id, pinned: bool):
    return (
        client.table("goals")
        .update({"pinned": pinned})
        .eq("id", goal_id)
        .execute()
        .data
    )


def count_pinned_goals(client, user_id):
    result = (
        client.table("goals")
        .select("id", count="exact")
        .eq("user_id", user_id)
        .eq("pinned", True)
        .execute()
    )
    return result.count or 0


# ---------------------------------------------------------------
# Sessions (goal progress log)
# ---------------------------------------------------------------
def log_session(client, user_id, goal_id):
    return (
        client.table("sessions")
        .insert({"user_id": user_id, "goal_id": goal_id})
        .execute()
        .data
    )


def get_last_session_date(client, goal_id):
    result = (
        client.table("sessions")
        .select("logged_at")
        .eq("goal_id", goal_id)
        .order("logged_at", desc=True)
        .limit(1)
        .execute()
        .data
    )
    if not result:
        return None
    # logged_at comes back as an ISO timestamp string
    return result[0]["logged_at"][:10]


# ---------------------------------------------------------------
# Gratitude entries
# ---------------------------------------------------------------
def get_today_gratitude(client, user_id, for_date: date):
    result = (
        client.table("gratitude_entries")
        .select("*")
        .eq("user_id", user_id)
        .eq("entry_date", for_date.isoformat())
        .execute()
        .data
    )
    return result[0] if result else None


def add_gratitude_entry(client, user_id, content, entry_date, entry_type="Personal"):
    return client.table("gratitude_entries").insert({
        "user_id": user_id,
        "content": content,
        "entry_date": entry_date.isoformat() if hasattr(entry_date, "isoformat") else str(entry_date),
        "type": entry_type,
    }).execute()


def get_gratitude_entries(client, user_id, filter_date: date = None):
    query = (
        client.table("gratitude_entries")
        .select("*")
        .eq("user_id", user_id)
        .order("entry_date", desc=True)
    )
    if filter_date:
        query = query.eq("entry_date", filter_date.isoformat())
    return query.execute().data

# --------------------------------------------------------------------------
# Counts for Home page
# --------------------------------------------------------------------------
def get_journal_count(client, user_id):
    resp = (
        client.table("journal_entries")
        .select("id", count="exact")
        .eq("user_id", user_id)
        .execute()
    )
    return resp.count or 0


def get_gratitude_count(client, user_id):
    resp = (
        client.table("gratitude_entries")
        .select("id", count="exact")
        .eq("user_id", user_id)
        .execute()
    )
    return resp.count or 0


def get_journal_entries_since(client, user_id, since_date):
    resp = (
        client.table("journal_entries")
        .select("*")
        .eq("user_id", user_id)
        .gte("entry_date", since_date.isoformat())
        .execute()
    )
    return resp.data or []