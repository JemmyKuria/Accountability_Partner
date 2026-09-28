"""
views/daily_hub.py — Home page.
Greeting, hero, KPI cards, Today's Focus, right rail.
"""

import random
from datetime import date, timedelta

import streamlit as st

from db import queries
from logic import business_logic as bl


CELEBRATIONS = ["Nailed it.", "That's a win.", "Right on target.", "Nice work."]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def _kpi_card(bg, icon_svg, label, value, unit, footer_html):
    return f"""
    <div class="ap-home-kpi" style="background:{bg};">
        <div>
            <div class="ap-home-kpi-top">
                <div class="ap-home-kpi-icon">{icon_svg}</div>
                <div class="ap-home-kpi-label">{label}</div>
            </div>
            <div class="ap-home-kpi-value">{value}</div>
            <div class="ap-home-kpi-unit">{unit}</div>
            <div class="ap-home-kpi-foot">{footer_html}</div>
        </div>
        <div class="ap-home-kpi-chevron">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2.4"
                 stroke-linecap="round" stroke-linejoin="round">
                <polyline points="9 18 15 12 9 6"/>
            </svg>
        </div>
    </div>
    """


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def render_home(client, user_id, user):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    # ---- Top row: greeting + date + avatar ----
    first_name = (user.email or "there").split("@")[0].split(".")[0].title()
    initials = (user.email or "AP")[:2].upper()

    st.markdown(
        f"""
        <div class="ap-home-top">
            <div>
                <div class="ap-greeting">Good morning, {first_name}</div>
                <div class="ap-greeting-sub">Small steps every day lead to big changes. You're doing great!</div>
            </div>
            <div class="ap-home-top-right">
                <div class="ap-date-chip">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                         stroke="currentColor" stroke-width="2"
                         stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="4" width="18" height="18" rx="2"/>
                        <path d="M16 2v4M8 2v4M3 10h18"/>
                    </svg>
                    {today.strftime("%a, %b %d, %Y")}
                </div>
                <div class="ap-avatar">{initials}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Hero banner ----
    st.markdown(
        """
        <div class="ap-hero">
            <div class="ap-hero-inner">
                <div class="ap-hero-title">Progress over perfection</div>
                <div class="ap-hero-sub">
                    You don't have to be perfect,<br>
                    you just have to keep showing up.
                </div>
                <div style="color:#7A9A6E;font-size:1.1rem;">♥</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Fetch data for KPIs ----
    goals = queries.get_goals(client, user_id)
    gratitude_count = queries.get_gratitude_count(client, user_id)
    journal_count = queries.get_journal_count(client, user_id)

    week_gratitude = queries.get_gratitude_entries(client, user_id, None)
    week_gratitude = [
        e for e in week_gratitude
        if _parse_date(e.get("entry_date")) and _parse_date(e["entry_date"]) >= week_start
    ]
    week_journal = queries.get_journal_entries_since(client, user_id, week_start)

    goals_done = 0
    total_goals = len(goals)
    for g in goals:
        if _goal_progress(g) >= 100:
            goals_done += 1

    # ---- KPI cards ----
    k1, k2, k3 = st.columns(3)

    with k1:
        st.markdown(_kpi_card(
            "#E8F1E2",
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#5A7A50" '
            'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/>'
            '<circle cx="12" cy="12" r="2"/></svg>',
            "Goals", total_goals, "total goals",
            f'<span class="ap-home-kpi-dot" style="background:#7A9A6E;"></span>{goals_done} completed<br>'
            f'<span class="ap-home-kpi-dot" style="background:#D4B96A;"></span>{max(total_goals - goals_done, 0)} in progress'
        ), unsafe_allow_html=True)

    with k2:
        st.markdown(_kpi_card(
            "#EDE7F5",
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7A5FA5" '
            'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
            "Gratitude", gratitude_count, "entries",
            f'Last entry: {_last_entry_label(week_gratitude)}'
        ), unsafe_allow_html=True)

    with k3:
        st.markdown(_kpi_card(
            "#F7F0DD",
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#A58535" '
            'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>'
            '<path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
            "Journal", journal_count, "entries",
            f'Last entry: {_last_entry_label(week_journal)}'
        ), unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    # ---- Two columns: focus + right rail ----
    left, right = st.columns([2, 1])

    with left:
        _render_todays_focus(client, user_id)

    with right:
        _render_right_rail(client, user_id, goals)


# --------------------------------------------------------------------------
# Today's Focus — non-negotiables for today
# --------------------------------------------------------------------------
def _render_todays_focus(client, user_id):
    today = date.today()
    tasks = queries.get_tasks_for_date(client, user_id, today, "non_negotiable")

    done_count = sum(1 for t in tasks if t["completed"])
    total = len(tasks)

    counter_html = (
        f'<span class="ap-section-head-link">{done_count} of {total} done</span>'
        if total else ""
    )

    st.markdown(
        f"""
        <div class="ap-section-head">
            <div class="ap-section-head-title">Today's Focus</div>
            {counter_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        if not tasks:
            st.caption("Nothing scheduled for today. Add your first focus below.")
        else:
            for task in tasks:
                checked = st.checkbox(
                    task["title"],
                    value=task["completed"],
                    key=f"focus_{task['id']}",
                )
                if checked != task["completed"]:
                    queries.set_task_completed(client, task["id"], checked)
                    if checked and task.get("tag"):
                        bl.link_task_completion_to_goal(client, user_id, task["tag"])
                    bl.refresh_streak_after_task_change(client, user_id)
                    if checked:
                        st.toast(random.choice(CELEBRATIONS))
                    st.rerun()

        # Inline add
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        with st.form("add_focus_form", clear_on_submit=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                new_title = st.text_input(
                    "New focus",
                    placeholder="Add a must-do for today...",
                    label_visibility="collapsed",
                )
            with c2:
                submitted = st.form_submit_button(
                    "Add", type="primary", use_container_width=True,
                )
            if submitted and new_title.strip():
                queries.add_task(
                    client, user_id,
                    new_title.strip(), "non_negotiable",
                    None, today,
                )
                st.rerun()


# --------------------------------------------------------------------------
# Right rail: upcoming + quote + recent gratitude
# --------------------------------------------------------------------------
def _render_right_rail(client, user_id, goals):
    st.markdown(
        """
        <div class="ap-section-head">
            <div class="ap-section-head-title">Upcoming</div>
            <span class="ap-section-head-link">View all</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    upcoming = [g for g in goals if _parse_date(g.get("deadline"))]
    upcoming.sort(key=lambda g: _parse_date(g["deadline"]))
    upcoming = upcoming[:4]

    if upcoming:
        html = ""
        for g in upcoming:
            dl = _parse_date(g["deadline"])
            html += f"""
            <div class="ap-upcoming-item">
                <div class="ap-upcoming-date">
                    <span class="d">{dl.strftime('%d')}</span>
                    <span class="m">{dl.strftime('%b')}</span>
                </div>
                <div class="ap-upcoming-body">
                    <div class="ap-upcoming-title">{g['title']}</div>
                    <div class="ap-upcoming-sub">{g.get('goal_type') or 'Personal'}</div>
                </div>
            </div>
            """
        with st.container(border=True):
            st.markdown(html, unsafe_allow_html=True)
    else:
        with st.container(border=True):
            st.caption("No upcoming deadlines.")

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="ap-quote-card" style="min-height:130px;">
            <div class="ap-quote-mark">"</div>
            <div class="ap-quote-text" style="font-size:0.98rem;">
                You're not just building habits, you're building the life you want.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="ap-section-head">
            <div class="ap-section-head-title">Recent Gratitude</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    entries = queries.get_gratitude_entries(client, user_id, None)[:3]

    if entries:
        html = ""
        for e in entries:
            ed = _parse_date(e.get("entry_date"))
            when = ed.strftime("%b %d, %Y") if ed else ""
            text = (e.get("content") or "")[:90]
            if len(e.get("content") or "") > 90:
                text += "…"
            html += f"""
            <div class="ap-recent-item">
                <div class="ap-recent-date">{when}</div>
                <div class="ap-recent-body">
                    <div class="ap-recent-text">{text}</div>
                </div>
            </div>
            """
        with st.container(border=True):
            st.markdown(html, unsafe_allow_html=True)
    else:
        with st.container(border=True):
            st.caption("No entries yet.")


# --------------------------------------------------------------------------
# Small utilities
# --------------------------------------------------------------------------
def _parse_date(val):
    if val is None:
        return None
    if isinstance(val, date):
        return val
    try:
        return date.fromisoformat(str(val))
    except Exception:
        return None


def _goal_progress(goal):
    if goal.get("progress_manual") is not None:
        return float(goal["progress_manual"])
    target = goal.get("total_sessions_target") or 1
    current = goal.get("current_sessions") or 0
    return min(current / target * 100, 100)


def _last_entry_label(entries):
    if not entries:
        return "No entries yet"
    dates = [_parse_date(e.get("entry_date")) for e in entries]
    dates = [d for d in dates if d]
    if not dates:
        return "—"
    return max(dates).strftime("%b %d, %Y")