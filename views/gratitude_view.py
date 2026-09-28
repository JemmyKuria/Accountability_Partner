"""
views/gratitude_view.py — Gratitude journal.
"""

from datetime import date

import streamlit as st

from db import queries


GRATITUDE_TYPES = ["Personal", "Relationship", "Career", "Health", "Travel", "Opportunity", "Small Win"]

TYPE_CLASS = {
    "Personal":     "ap-gtype-personal",
    "Relationship": "ap-gtype-relationship",
    "Career":       "ap-gtype-career",
    "Health":       "ap-gtype-health",
    "Travel":       "ap-gtype-travel",
    "Opportunity":  "ap-gtype-opportunity",
    "Small Win":    "ap-gtype-small-win",
}


def _type_pill(t):
    cls = TYPE_CLASS.get(t or "Personal", "ap-gtype-personal")
    return f'<span class="ap-pill-sm {cls}">{t or "Personal"}</span>'


def render_gratitude_archive(client, user_id):
    # Reset counter — used to force widget reset when "Clear Filters" is clicked.
    if "g_reset" not in st.session_state:
        st.session_state["g_reset"] = 0
    reset_key = st.session_state["g_reset"]

    # ---------- Header ----------
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<div class="ap-page-title">Gratitude</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="ap-page-sub">Notice the good. It changes everything.</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div style="text-align:right;font-family:Caveat,cursive;font-size:1.35rem;'
            'color:#7A9A6E;line-height:1.25;padding-top:14px;">'
            'Gratitude<br>builds a happier<br>you ♡</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # ---------- Add-entry card ----------
    with st.container(border=True):
        head_left, head_right = st.columns([3, 1])
        with head_left:
            st.markdown(
                '<div style="display:flex;align-items:center;gap:14px;">'
                '<div style="width:44px;height:44px;border-radius:12px;background:#E8F1E2;'
                'display:flex;align-items:center;justify-content:center;flex-shrink:0;">'
                '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#5A7A50" '
                'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
                '<circle cx="12" cy="12" r="4"/>'
                '<path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>'
                '</svg></div>'
                '<div>'
                '<div style="font-family:Fraunces,serif;font-size:1.1rem;font-weight:600;color:#2A2A2A;">'
                'What are you grateful for today?</div>'
                '<div style="color:#9A9A9A;font-size:0.83rem;margin-top:2px;">'
                'Take a moment to notice the good, big or small.</div>'
                '</div></div>',
                unsafe_allow_html=True,
            )
        with head_right:
            st.markdown(
                f'<div style="text-align:right;padding-top:12px;">'
                f'<span style="display:inline-flex;align-items:center;gap:8px;'
                f'background:#F7F5F0;border:1px solid #E8E5DC;border-radius:8px;'
                f'padding:6px 12px;color:#6B6B6B;font-size:0.82rem;font-weight:500;">'
                f'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6B6B6B" '
                f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
                f'<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>'
                f'</svg>{date.today().strftime("%b %d, %Y")}</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

        with st.form("add_gratitude_form", clear_on_submit=True):
            content = st.text_area(
                "Entry",
                placeholder="e.g. I'm grateful for my health, my family, new opportunities...",
                height=100,
                label_visibility="collapsed",
            )
            c1, c2 = st.columns([3, 1.2])
            with c1:
                gt = st.selectbox("Type of Gratitude", GRATITUDE_TYPES, label_visibility="collapsed")
            with c2:
                submitted = st.form_submit_button("Save Gratitude", type="primary", use_container_width=True)

            if submitted:
                if not content.strip():
                    st.error("Write something first.")
                else:
                    queries.add_gratitude_entry(client, user_id, content.strip(), date.today(), gt)
                    st.rerun()

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    # ---------- Filters ----------
    with st.container(border=True):
        st.markdown(
            '<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">'
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6B6B6B" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>'
            '<span style="font-family:Fraunces,serif;font-size:1rem;font-weight:600;color:#2A2A2A;">Filters</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        f1, f2, f3, f4 = st.columns([1.2, 1.2, 1.2, 1])

        with f1:
            st.markdown('<div style="color:#9A9A9A;font-size:0.75rem;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;margin-bottom:6px;">From</div>', unsafe_allow_html=True)
            from_date = st.date_input(
                "From", value=None, label_visibility="collapsed",
                key=f"g_from_{reset_key}",
            )

        with f2:
            st.markdown('<div style="color:#9A9A9A;font-size:0.75rem;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;margin-bottom:6px;">To</div>', unsafe_allow_html=True)
            to_date = st.date_input(
                "To", value=None, label_visibility="collapsed",
                key=f"g_to_{reset_key}",
            )

        with f3:
            st.markdown('<div style="color:#9A9A9A;font-size:0.75rem;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;margin-bottom:6px;">Type</div>', unsafe_allow_html=True)
            type_filter = st.selectbox(
                "Type", ["All Types"] + GRATITUDE_TYPES,
                label_visibility="collapsed",
                key=f"g_type_{reset_key}",
            )

        with f4:
            st.markdown("<div style='height:22px;'></div>", unsafe_allow_html=True)
            if st.button("Clear Filters", use_container_width=True, key=f"g_clear_{reset_key}"):
                # Incrementing the reset key remounts all filter widgets
                # with fresh keys, which resets them to their defaults.
                st.session_state["g_reset"] += 1
                st.rerun()

    # ---------- Load & filter entries ----------
    entries = queries.get_gratitude_entries(client, user_id, None)

    filtered = []
    for e in entries:
        ed = e.get("entry_date")
        try:
            ed_parsed = ed if isinstance(ed, date) else date.fromisoformat(str(ed))
        except Exception:
            ed_parsed = None

        if from_date and ed_parsed and ed_parsed < from_date:
            continue
        if to_date and ed_parsed and ed_parsed > to_date:
            continue
        if type_filter != "All Types" and (e.get("type") or "Personal") != type_filter:
            continue
        filtered.append(e)

    # ---------- Journal header ----------
    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    h1, h2 = st.columns([3, 1])
    with h1:
        st.markdown(
            '<div style="font-family:Fraunces,serif;font-size:1.35rem;font-weight:600;color:#2A2A2A;">'
            'My Gratitude Journal</div>',
            unsafe_allow_html=True,
        )
    with h2:
        st.markdown(
            f'<div style="text-align:right;color:#9A9A9A;font-size:0.82rem;padding-top:10px;">'
            f'Total entries: <strong style="color:#6B6B6B;">{len(filtered)}</strong></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ---------- Table ----------
    if not filtered:
        st.info("No entries match the current filters.")
    else:
        rows = ""
        for e in filtered:
            ed = e.get("entry_date")
            try:
                ed_str = (ed if isinstance(ed, date) else date.fromisoformat(str(ed))).strftime("%b %d, %Y")
            except Exception:
                ed_str = str(ed or "—")
            gt = e.get("type") or "Personal"
            rows += f"""
            <tr>
                <td style="color:#6B6B6B;white-space:nowrap;">{ed_str}</td>
                <td class="ap-goal-title-cell">{e['content']}</td>
                <td>{_type_pill(gt)}</td>
                <td style="width:32px;color:#9A9A9A;text-align:center;cursor:pointer;">···</td>
            </tr>
            """

        st.markdown(
            f"""
            <div class="ap-table-wrap">
                <table class="ap-goals-table">
                    <thead>
                        <tr>
                            <th style="width:140px;">Date</th>
                            <th>What I'm Grateful For</th>
                            <th style="width:140px;">Type</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------- Manage ----------
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    with st.expander(f"Manage entries ({len(filtered)})"):
        if not filtered:
            st.caption("Nothing to manage.")
        for e in filtered:
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{e.get('entry_date')}** · {e.get('type') or 'Personal'}")
                    st.write(e["content"])
                with c2:
                    if st.button("Delete", key=f"delg_{e['id']}", use_container_width=True):
                        client.table("gratitude_entries").delete().eq("id", e["id"]).execute()
                        st.rerun()