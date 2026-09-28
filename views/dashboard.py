"""
views/dashboard.py — Goals page.
Matches the mockup: filter tabs, add-goal card, pastel KPIs, goals table.
"""

from datetime import date, timedelta

import streamlit as st

from db import queries
from logic import business_logic as bl


GOAL_TYPES = ["Financial", "Health", "Learning", "Career", "Personal", "Relationship", "Project"]
PRIORITIES = ["High", "Medium", "Low"]


# ---------- Helpers ----------

def _status_from_progress(p):
    if p >= 100:
        return "Done"
    if p <= 0:
        return "Not Started"
    return "In Progress"


def _type_class(t):
    return {
        "Financial": "ap-type-financial",
        "Health": "ap-type-health",
        "Learning": "ap-type-learning",
        "Career": "ap-type-career",
        "Personal": "ap-type-personal",
        "Relationship": "ap-type-relationship",
        "Project": "ap-type-project",
    }.get(t, "ap-type-default")


def _priority_class(p):
    return {
        "High": "ap-priority-high",
        "Medium": "ap-priority-medium",
        "Low": "ap-priority-low",
    }.get(p, "ap-priority-medium")


def _status_class(s):
    return {
        "Done": "ap-status-done",
        "In Progress": "ap-status-in-progress",
        "Not Started": "ap-status-not-started",
    }.get(s, "ap-status-not-started")


def _kpi_pastel(bg, icon_svg, label, value):
    return f"""
    <div class="ap-kpi-pastel" style="background:{bg};">
        <div class="ap-kpi-pastel-icon">{icon_svg}</div>
        <div class="ap-kpi-pastel-body">
            <div class="ap-kpi-pastel-label">{label}</div>
            <div class="ap-kpi-pastel-value">{value}</div>
        </div>
    </div>
    """


def _in_period(deadline, period):
    """Filter helper for the top tabs."""
    if period == "All Goals":
        return True
    if period == "Other":
        return deadline is None
    if deadline is None:
        return False
    days = (deadline - date.today()).days
    if period == "Daily":
        return 0 <= days <= 1
    if period == "Weekly":
        return 0 <= days <= 7
    if period == "Monthly":
        return 0 <= days <= 30
    return True


# ---------- Main ----------

def render_dashboard(client, user_id):
    # Header
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<div class="ap-page-title">Goals</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="ap-page-sub">Set your goals, track your progress, and keep building the life you want.</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div style="text-align:right;font-family:Caveat,cursive;font-size:1.4rem;'
            'color:#7A9A6E;line-height:1.2;padding-top:14px;">Progress,<br>not perfection.</div>',
            unsafe_allow_html=True,
        )

    # Filter tabs
    period = st.radio(
        "Period",
        ["All Goals", "Daily", "Weekly", "Monthly", "Other"],
        horizontal=True,
        label_visibility="collapsed",
        key="goal_period",
    )

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # Add-goal card
    with st.container(border=True):
        st.markdown(
            '<div style="font-family:Fraunces,serif;font-size:1.15rem;font-weight:600;'
            'color:#2A2A2A;margin-bottom:2px;">Add a New Goal</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="color:#9A9A9A;font-size:0.85rem;margin-bottom:16px;">'
            'What do you want to achieve?</div>',
            unsafe_allow_html=True,
        )

        with st.form("add_goal_form", clear_on_submit=True):
            c1, c2, c3, c4, c5 = st.columns([3, 1.2, 1.2, 1.2, 1])
            with c1:
                title = st.text_input("Title", placeholder="e.g. Save 5k this month", label_visibility="collapsed")
            with c2:
                goal_type = st.selectbox("Type", GOAL_TYPES, label_visibility="collapsed")
            with c3:
                priority = st.selectbox("Priority", PRIORITIES, index=1, label_visibility="collapsed")
            with c4:
                deadline = st.date_input("Due date", value=None, label_visibility="collapsed")
            with c5:
                submitted = st.form_submit_button("Add Goal +", type="primary", use_container_width=True)

            description = st.text_input(
                "Description",
                placeholder="Add a short description (optional)...",
                label_visibility="collapsed",
            )

            if submitted and title.strip():
                queries.add_goal(
                    client, user_id,
                    title=title.strip(),
                    deadline=deadline if isinstance(deadline, date) else None,
                    tag=None,
                    total_sessions_target=100,
                    goal_type=goal_type,
                    priority=priority,
                    description=description.strip() or None,
                )
                st.rerun()

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # Load goals
    goals = queries.get_goals(client, user_id)
    if not goals:
        st.info("No goals yet — add your first one above.")
        return

    # Compute stats
    def _progress(g):
        return bl.get_progress_percentage(g)

    total = len(goals)
    done = sum(1 for g in goals if _progress(g) >= 100)
    in_prog = sum(1 for g in goals if 0 < _progress(g) < 100)
    not_started = sum(1 for g in goals if _progress(g) <= 0)

    # KPI row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(_kpi_pastel(
            "#E8F1E2",
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#5A7A50" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M9 7h6M9 11h6M9 15h4"/></svg>',
            "Total Goals", total,
        ), unsafe_allow_html=True)
    with k2:
        st.markdown(_kpi_pastel(
            "#E5F0E0",
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4A7A4A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
            "Completed", done,
        ), unsafe_allow_html=True)
    with k3:
        st.markdown(_kpi_pastel(
            "#EDE7F5",
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7A5FA5" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
            "In Progress", in_prog,
        ), unsafe_allow_html=True)
    with k4:
        st.markdown(_kpi_pastel(
            "#F5E2E2",
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#A55555" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/></svg>',
            "Not Started", not_started,
        ), unsafe_allow_html=True)

    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

    # Your Goals header + filter row
    h1, h2, h3 = st.columns([2, 1, 1.5])
    with h1:
        st.markdown(
            '<div style="font-family:Fraunces,serif;font-size:1.35rem;font-weight:600;'
            'color:#2A2A2A;padding-top:8px;">Your Goals</div>',
            unsafe_allow_html=True,
        )
    with h2:
        status_filter = st.selectbox(
            "Status", ["All Statuses", "Done", "In Progress", "Not Started"],
            label_visibility="collapsed", key="goal_status_filter",
        )
    with h3:
        search = st.text_input(
            "Search", placeholder="Search goals...",
            label_visibility="collapsed", key="goal_search",
        )

    # Filter goals
    filtered = []
    for g in bl.sort_goals_for_dashboard(client, goals):
        dl = None
        if g.get("deadline"):
            try:
                dl = date.fromisoformat(str(g["deadline"]))
            except Exception:
                dl = None
        if not _in_period(dl, period):
            continue
        p = _progress(g)
        s = _status_from_progress(p)
        if status_filter != "All Statuses" and s != status_filter:
            continue
        if search and search.lower() not in f"{g['title']} {g.get('description','')}".lower():
            continue
        filtered.append(g)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # Table
    if not filtered:
        st.info("No goals match the current filters.")
    else:
        rows = ""
        for g in filtered:
            p = _progress(g)
            s = _status_from_progress(p)
            gt = g.get("goal_type") or "Personal"
            pr = g.get("priority") or "Medium"
            dl = g.get("deadline") or "—"
            desc = g.get("description") or ""
            desc_html = f'<div class="ap-goal-desc">{desc}</div>' if desc else ""

            rows += f"""
            <tr>
                <td style="width:32px;">
                    <input type="checkbox" style="width:16px;height:16px;accent-color:#7A9A6E;cursor:pointer;">
                </td>
                <td class="ap-goal-title-cell">
                    <div>{g['title']}</div>
                    {desc_html}
                </td>
                <td><span class="ap-pill-sm {_type_class(gt)}">{gt}</span></td>
                <td><span class="ap-pill-sm {_priority_class(pr)}">{pr}</span></td>
                <td style="color:#6B6B6B;">{dl}</td>
                <td><span class="ap-pill-sm {_status_class(s)}">{s}</span></td>
                <td style="width:32px;color:#9A9A9A;text-align:center;cursor:pointer;">···</td>
            </tr>
            """

        st.markdown(
            f"""
            <div class="ap-table-wrap">
                <table class="ap-goals-table">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Goal</th>
                            <th>Type</th>
                            <th>Priority</th>
                            <th>Due Date</th>
                            <th>Status</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Manage (functional actions live here, below the clean table)
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    with st.expander(f"Manage goals ({len(filtered)})"):
        for g in filtered:
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{g['title']}**")
                    meta = []
                    if g.get("deadline"):
                        meta.append(f"Due {g['deadline']}")
                    if g.get("priority"):
                        meta.append(g["priority"])
                    if meta:
                        st.caption(" · ".join(meta))
                with c2:
                    pin_label = "Unpin" if g["pinned"] else "Pin"
                    if st.button(pin_label, key=f"pin_{g['id']}", use_container_width=True):
                        queries.set_goal_pinned(client, g["id"], not g["pinned"])
                        st.rerun()

                prog = _progress(g)
                st.progress(min(int(prog), 100) / 100.0)

                c3, c4, c5 = st.columns([3, 1, 1])
                with c3:
                    new_p = st.slider(
                        "Adjust", 0, 100, int(prog),
                        key=f"slider_{g['id']}", label_visibility="collapsed",
                    )
                    if new_p != int(prog):
                        queries.set_goal_manual_progress(client, g["id"], float(new_p))
                        st.rerun()
                with c4:
                    if st.button("Log Session", key=f"log_{g['id']}", use_container_width=True, type="primary"):
                        queries.log_session(client, user_id, g["id"])
                        queries.update_goal_sessions(client, g["id"], g.get("current_sessions", 0) + 1)
                        st.rerun()
                with c5:
                    if st.button("Delete", key=f"del_{g['id']}", use_container_width=True):
                        # Add a delete_goal function in queries if you don't have one
                        client.table("goals").delete().eq("id", g["id"]).execute()
                        st.rerun()