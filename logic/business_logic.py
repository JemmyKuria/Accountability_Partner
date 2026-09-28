"""
Business rules that don't belong in the UI layer or the raw
queries layer: streak math, weekly scoring, tag-based auto-linking
between tasks and goals, and the dashboard sort order.
"""
from datetime import date, timedelta

from db import queries


# ---------------------------------------------------------------
# Streak
# ---------------------------------------------------------------
def sync_streak_on_load(client, user_id):
    """
    Call once when the Daily Hub loads. Handles the 'missed a day'
    reset: if the last fully-completed day isn't today or yesterday,
    the streak is broken and resets to 0.
    """
    streak_row = queries.get_streak(client, user_id)
    last_completed = streak_row.get("last_completed_date")
    if not last_completed:
        return streak_row

    last_completed_date = date.fromisoformat(last_completed)
    today = date.today()
    yesterday = today - timedelta(days=1)

    if last_completed_date not in (today, yesterday):
        queries.upsert_streak(client, user_id, 0, None)
        streak_row["current_streak"] = 0
        streak_row["last_completed_date"] = None

    return streak_row


def refresh_streak_after_task_change(client, user_id):
    """
    Call after any Non-Negotiable is checked/unchecked. Recomputes
    whether all of today's Non-Negotiables are done, and adjusts
    the streak accordingly:
      - all done, not yet counted today -> +1, mark today as completed
      - no longer all done, today was previously counted -> -1, clear mark
    """
    today = date.today()
    non_negotiables = queries.get_tasks_for_date(client, user_id, today, "non_negotiable")
    all_done_today = bool(non_negotiables) and all(t["completed"] for t in non_negotiables)

    streak_row = queries.get_streak(client, user_id)
    current_streak = streak_row["current_streak"]
    last_completed = streak_row.get("last_completed_date")
    already_counted_today = last_completed == today.isoformat()

    if all_done_today and not already_counted_today:
        current_streak += 1
        queries.upsert_streak(client, user_id, current_streak, today)
    elif not all_done_today and already_counted_today:
        current_streak = max(0, current_streak - 1)
        queries.upsert_streak(client, user_id, current_streak, None)

    return current_streak


# ---------------------------------------------------------------
# Weekly score
# ---------------------------------------------------------------
def get_week_bounds(reference_date: date, weeks_ago: int = 0):
    """Returns (monday, sunday) for the week `weeks_ago` weeks before
    the week containing reference_date. weeks_ago=0 is the current week."""
    start_of_this_week = reference_date - timedelta(days=reference_date.weekday())
    monday = start_of_this_week - timedelta(weeks=weeks_ago)
    sunday = monday + timedelta(days=6)
    return monday, sunday


def get_weekly_scores(client, user_id):
    today = date.today()
    this_week_start, this_week_end = get_week_bounds(today, 0)
    last_week_start, last_week_end = get_week_bounds(today, 1)

    this_week_count = queries.get_weekly_bonus_count(
        client, user_id, this_week_start, this_week_end
    )
    last_week_count = queries.get_weekly_bonus_count(
        client, user_id, last_week_start, last_week_end
    )
    return this_week_count * 10, last_week_count * 10


# ---------------------------------------------------------------
# Tag-based auto-linking
# ---------------------------------------------------------------
def link_task_completion_to_goal(client, user_id, tag):
    """
    When a tagged task is completed, find a goal with the same tag
    for this user and bump its session count by one.
    Returns the updated goal dict, or None if no matching goal.
    """
    if not tag:
        return None

    goals = queries.get_goals(client, user_id)
    matching = next((g for g in goals if g.get("tag") == tag), None)
    if not matching:
        return None

    new_sessions = matching["current_sessions"] + 1
    queries.update_goal_sessions(client, matching["id"], new_sessions)
    queries.log_session(client, user_id, matching["id"])
    matching["current_sessions"] = new_sessions
    return matching


def get_progress_percentage(goal):
    if goal.get("progress_manual") is not None:
        return goal["progress_manual"]
    target = goal.get("total_sessions_target") or 1
    return min(100.0, (goal.get("current_sessions", 0) / target) * 100)


# ---------------------------------------------------------------
# Dashboard sort: pinned -> needs-attention -> urgency
# ---------------------------------------------------------------
def sort_goals_for_dashboard(client, goals):
    today = date.today()
    enriched = []
    for g in goals:
        last_session = queries.get_last_session_date(client, g["id"])
        needs_attention = False
        if last_session:
            days_since = (today - date.fromisoformat(last_session)).days
            needs_attention = days_since > 14
        elif g.get("created_at"):
            # never logged a session at all — treat as needing attention
            created = date.fromisoformat(g["created_at"][:10])
            needs_attention = (today - created).days > 14

        days_remaining = None
        if g.get("deadline"):
            days_remaining = (date.fromisoformat(g["deadline"]) - today).days

        enriched.append(
            {**g, "needs_attention": needs_attention, "days_remaining": days_remaining}
        )

    pinned = sorted(
        [g for g in enriched if g["pinned"]],
        key=lambda g: g["days_remaining"] if g["days_remaining"] is not None else 9999,
    )
    attention = sorted(
        [g for g in enriched if not g["pinned"] and g["needs_attention"]],
        key=lambda g: g["days_remaining"] if g["days_remaining"] is not None else 9999,
    )
    rest = sorted(
        [g for g in enriched if not g["pinned"] and not g["needs_attention"]],
        key=lambda g: g["days_remaining"] if g["days_remaining"] is not None else 9999,
    )
    return pinned + attention + rest