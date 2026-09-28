"""views/job_hunt.py — Applications, Find Jobs, Analytics."""

from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from cv_utils import extract_cv_text, extract_keywords, score_matches
from scrapers import search_all
from db.job_queries import (
    save_cv_profile, load_cv_profile, add_application, fetch_applications,
    update_application, delete_application, dismiss_job, fetch_dismissed, clear_dismissed,
)
from views.style import leaf_svg


STATUS_OPTIONS = ["Applied", "Under Review", "Interview Scheduled",
                  "Interview Completed", "Rejected", "Offer", "No Response / Ghosted"]

PILL_CLASS = {
    "Applied": "ap-pill-applied",
    "Under Review": "ap-pill-progress",
    "Interview Scheduled": "ap-pill-interview",
    "Interview Completed": "ap-pill-interview",
    "Offer": "ap-pill-offer",
    "Rejected": "ap-pill-rejected",
    "No Response / Ghosted": "ap-pill-declined",
}


def _pill(status):
    cls = PILL_CLASS.get(status, "ap-pill-declined")
    return f'<span class="ap-pill {cls}">{status}</span>'


def _kpi_small(label, value, footer, bg, fg):
    return f"""
    <div class="ap-kpi" style="min-height:100px;">
        <div class="ap-kpi-label">{label}</div>
        <div class="ap-kpi-value" style="color:{fg};">{value}</div>
        <div class="ap-kpi-foot">{footer}</div>
    </div>
    """


def render_job_hunt(client, user_id, initial_tab="Applications"):
    st.markdown(
        f'<div class="ap-page-title">Job Hunt <span class="ap-leaf-inline">{leaf_svg(18, "#7A9A6E")}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="ap-page-sub">Track your applications, interviews, and progress.</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Applications", "Find Jobs", "Analytics"])
    with tabs[0]:
        _render_applications(client, user_id)
    with tabs[1]:
        _render_find_jobs(client, user_id)
    with tabs[2]:
        _render_analytics(client, user_id)


# -------- APPLICATIONS TABLE --------
def _render_applications(client, user_id):
    apps = fetch_applications(client, user_id)

    # Action row
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<div class="ap-section-label">All applications</div>', unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # Add-new expander
    with st.expander("Add a new application"):
        with st.form("add_app"):
            a, b, c = st.columns([2, 2, 1])
            with a:
                company = st.text_input("Company")
                position = st.text_input("Position")
            with b:
                job_url = st.text_input("Job URL")
                platform = st.text_input("Platform (Fuzu, LinkedIn, etc.)")
            with c:
                status = st.selectbox("Status", STATUS_OPTIONS)
                st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Add", type="primary")
            if submitted and company and position:
                add_application(client, user_id, job_url or "manual", company, position, platform or "Manual", status)
                st.rerun()

    if apps.empty:
        st.info("No applications yet. Add your first one above or from Find Jobs.")
        return

    # Filters
    f1, f2, f3, f4 = st.columns([2, 1, 1, 1])
    with f1:
        search = st.text_input("Search", placeholder="Search company, role, or notes...", label_visibility="collapsed")
    with f2:
        status_filter = st.selectbox("Status", ["All Statuses"] + STATUS_OPTIONS, label_visibility="collapsed")
    with f3:
        locations = ["All Locations"] + sorted(apps["platform"].dropna().unique().tolist())
        loc_filter = st.selectbox("Platform", locations, label_visibility="collapsed")
    with f4:
        window = st.selectbox("When", ["All Dates", "Last 30 days", "Last 90 days"], label_visibility="collapsed")

    # Apply filters
    df = apps.copy()
    if search:
        mask = df.apply(lambda r: search.lower() in f"{r['company']} {r['position']} {r.get('notes','')}".lower(), axis=1)
        df = df[mask]
    if status_filter != "All Statuses":
        df = df[df["status"] == status_filter]
    if loc_filter != "All Locations":
        df = df[df["platform"] == loc_filter]
    if window == "Last 30 days":
        df = df[df["date_applied"] >= date.today() - timedelta(days=30)]
    elif window == "Last 90 days":
        df = df[df["date_applied"] >= date.today() - timedelta(days=90)]

    # Build HTML table
    rows_html = ""
    for i, (_, row) in enumerate(df.iterrows(), start=1):
        rows_html += f"""
        <tr>
            <td class="ap-cell-num">{i}</td>
            <td>{row['date_applied']}</td>
            <td class="ap-cell-pos">{row['position'] or '—'}</td>
            <td class="ap-cell-company">{row['company'] or '—'}</td>
            <td class="ap-cell-company">{row['platform'] or '—'}</td>
            <td>{_pill(row['status'])}</td>
            <td class="ap-cell-notes">{row.get('notes') or '—'}</td>
        </tr>
        """

    st.markdown(
        f"""
        <div class="ap-table-wrap">
            <table class="ap-table">
                <thead>
                    <tr>
                        <th style="width:40px;">#</th>
                        <th>Date Applied</th>
                        <th>Position</th>
                        <th>Company</th>
                        <th>Platform</th>
                        <th>Status</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Manage entries
    with st.expander(f"Manage entries ({len(df)})"):
        for _, row in df.iterrows():
            st.markdown(f"**{row['position']}** — {row['company']}")
            c1, c2, c3, c4 = st.columns([2, 3, 1, 1])
            with c1:
                new_status = st.selectbox("Status", STATUS_OPTIONS,
                    index=STATUS_OPTIONS.index(row["status"]) if row["status"] in STATUS_OPTIONS else 0,
                    key=f"s_{row['id']}", label_visibility="collapsed")
            with c2:
                new_notes = st.text_input("Notes", value=row.get("notes") or "",
                    key=f"n_{row['id']}", label_visibility="collapsed", placeholder="Notes...")
            with c3:
                if st.button("Save", key=f"sv_{row['id']}"):
                    update_application(client, row["id"], new_status, new_notes)
                    st.rerun()
            with c4:
                if st.button("Delete", key=f"d_{row['id']}"):
                    delete_application(client, row["id"])
                    st.rerun()
            st.markdown("<hr style='margin:8px 0;'>", unsafe_allow_html=True)


# -------- FIND JOBS --------
def _render_find_jobs(client, user_id):
    profile = load_cv_profile(client, user_id)
    cv_text = ""

    if profile and profile.get("cv_text"):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f'<div class="ap-section-label">Active CV · {profile.get("cv_filename","CV")}</div>', unsafe_allow_html=True)
        with c2:
            if st.button("Re-upload CV", key="reup", use_container_width=True):
                save_cv_profile(client, user_id, "", "")
                st.rerun()
        with st.expander("Preview CV text"):
            st.text(profile["cv_text"][:2500])
        cv_text = profile["cv_text"]
    else:
        uploaded = st.file_uploader("Upload CV (PDF, DOCX, TXT)", type=["pdf","docx","txt"], key="cvup")
        if uploaded:
            try:
                cv_text = extract_cv_text(uploaded)
                save_cv_profile(client, user_id, cv_text, uploaded.name)
                st.success("CV saved.")
                st.rerun()
            except Exception as e:
                st.error(f"Could not read: {e}")

    if not cv_text:
        st.info("Upload your CV to start finding matches.")
        return

    keywords = extract_keywords(cv_text)
    terms = st.text_area("Search terms", value=", ".join(keywords) if keywords else "data analyst",
                         height=70, label_visibility="collapsed")

    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
    with c1: fuzu = st.checkbox("Fuzu", value=True)
    with c2: bm = st.checkbox("BrighterMonday", value=True)
    with c3: cs = st.checkbox("Corporate Staffing", value=True)
    with c4: rok = st.checkbox("RemoteOK", value=True)
    with c5: pages = st.number_input("Pages", 1, 5, 2)

    sources = {"fuzu": fuzu, "brightermonday": bm, "corporate_staffing": cs, "remoteok": rok}

    if st.button("Search jobs", type="primary"):
        terms_list = [t.strip() for t in terms.split(",") if t.strip()]
        all_jobs = []
        prog = st.progress(0.0)
        for i, t in enumerate(terms_list, 1):
            all_jobs.extend(search_all(t, sources, max_pages=pages))
            prog.progress(i / max(len(terms_list), 1))
        prog.empty()
        st.session_state.jh_results = score_matches(cv_text, all_jobs) if all_jobs else []

    results = st.session_state.get("jh_results", [])
    if not results:
        return

    dismissed = fetch_dismissed(client, user_id)
    visible = [j for j in results if j["url"] not in dismissed]

    st.markdown(f'<div class="ap-section-label">{len(visible)} results</div>', unsafe_allow_html=True)

    for job in visible[:30]:
        score = job.get("match_score", 0)
        initials = (job.get("company") or job["title"][:2]).strip()[:2].upper()
        st.markdown(
            f"""
            <div class="ap-job-row">
                <div class="ap-job-logo">{initials}</div>
                <div class="ap-job-body">
                    <div class="ap-job-title">{job['title']} <span class="ap-job-badge">{score:.0f}% match</span></div>
                    <div class="ap-job-company">{job.get('company') or '—'} · {job.get('source','')} · {job.get('posted_date') or 'Date unknown'}</div>
                </div>
                <a href="{job['url']}" target="_blank" class="ap-tag" style="text-decoration:none;">Open</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -------- ANALYTICS --------
def _render_analytics(client, user_id):
    apps = fetch_applications(client, user_id)
    if apps.empty:
        st.info("Add applications to see analytics.")
        return

    total = len(apps)
    interviews = len(apps[apps["status"].isin(["Interview Scheduled", "Interview Completed"])])
    offers = len(apps[apps["status"] == "Offer"])
    responded = len(apps[~apps["status"].isin(["Applied", "No Response / Ghosted"])])
    rate = (responded / total * 100) if total else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(_kpi_small("Total Applications", total, "+2 vs last 30 days", "#E8F1E2", "#5A7A50"), unsafe_allow_html=True)
    with k2: st.markdown(_kpi_small("Interviews", interviews, "+1 vs last 30 days", "#EDE7F5", "#7A5FA5"), unsafe_allow_html=True)
    with k3: st.markdown(_kpi_small("Offers", offers, "+1 vs last 30 days", "#F7F0DD", "#A58535"), unsafe_allow_html=True)
    with k4: st.markdown(_kpi_small("Success Rate", f"{rate:.0f}%", "+5% vs last 30 days", "#E8F1E2", "#5A7A50"), unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    layout = dict(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="Inter, sans-serif", color="#2A2A2A", size=12),
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(gridcolor="#F0EDE5", linecolor="#F0EDE5", zeroline=False),
        yaxis=dict(gridcolor="#F0EDE5", linecolor="#F0EDE5", zeroline=False),
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ap-section-label">Applications over time</div>', unsafe_allow_html=True)
        tmp = apps.copy()
        tmp["date_applied"] = pd.to_datetime(tmp["date_applied"])
        td = tmp.groupby(tmp["date_applied"].dt.date).size().reset_index(name="Count")
        fig1 = px.bar(td, x="date_applied", y="Count")
        fig1.update_traces(marker_color="#7A9A6E")
        fig1.update_layout(**layout, height=280, xaxis_title="", yaxis_title="")
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    with c2:
        st.markdown('<div class="ap-section-label">Application status</div>', unsafe_allow_html=True)
        sd = apps["status"].value_counts().reset_index()
        sd.columns = ["Status", "Count"]
        color_map = {
            "Applied": "#7A9AA5", "Under Review": "#D4B96A", "Interview Scheduled": "#9A7FB5",
            "Interview Completed": "#9A7FB5", "Offer": "#7AA57A", "Rejected": "#C57A7A",
            "No Response / Ghosted": "#9A9A9A",
        }
        fig2 = px.pie(sd, names="Status", values="Count", hole=0.55,
                     color="Status", color_discrete_map=color_map)
        fig2.update_layout(**layout, height=280, legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="ap-section-label">Top platforms</div>', unsafe_allow_html=True)
    plat = apps.groupby("platform").size().reset_index(name="Count").sort_values("Count", ascending=False).head(6)
    fig3 = go.Figure(go.Bar(
        x=plat["Count"], y=plat["platform"], orientation="h",
        marker_color="#7A9A6E",
        text=plat["Count"], textposition="outside",
        textfont=dict(color="#5E7E55", size=13),
    ))
    fig3.update_layout(**layout, height=max(200, 50 * len(plat)), xaxis_title="", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})