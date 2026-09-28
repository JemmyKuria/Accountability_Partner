import streamlit as st

from db.supabase_client import get_client, set_user_session
from views.style import inject_custom_css, leaf_svg
from views.auth_view import render_auth
from views.daily_hub import render_home
from views.dashboard import render_dashboard
from views.gratitude_view import render_gratitude_archive
from views.job_hunt import render_job_hunt
from views.profile import render_profile


st.set_page_config(
    page_title="Accountability",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


NAV_ITEMS = [
    ("Home",         ":material/home:"),
    ("Goals",        ":material/target:"),
    ("Gratitude",    ":material/favorite:"),
    ("Applications", ":material/work:"),
    ("Profile",      ":material/person:"),
]


def get_or_create_client():
    if "supabase_client" not in st.session_state:
        st.session_state["supabase_client"] = get_client()
    client = st.session_state["supabase_client"]

    if st.session_state.get("access_token"):
        try:
            set_user_session(
                client,
                st.session_state["access_token"],
                st.session_state["refresh_token"],
            )
        except Exception:
            for key in ("user", "access_token", "refresh_token"):
                st.session_state.pop(key, None)

    return client


def _sidebar_brand():
    st.markdown(
        f"""
        <div class="ap-brand">
            <div class="ap-brand-mark">{leaf_svg(28, "#7A9A6E")}</div>
            <div class="ap-brand-text">
                <span class="ap-brand-name">Accountability</span>
                <span class="ap-brand-sub">Personal OS</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    inject_custom_css()
    client = get_or_create_client()

    if not st.session_state.get("user"):
        render_auth(client)
        return

    user_id = st.session_state["user"].id

    # Current page (persisted across reruns)
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    with st.sidebar:
        _sidebar_brand()

        # Nav as buttons — active item uses type="primary"
        for label, icon in NAV_ITEMS:
            is_active = st.session_state["page"] == label
            btn_type = "primary" if is_active else "secondary"
            if st.button(
                label,
                key=f"nav_{label}",
                type=btn_type,
                icon=icon,
                use_container_width=True,
            ):
                st.session_state["page"] = label
                st.rerun()

        st.markdown(
            '<div class="ap-side-quote">"Small steps create<br>big results."</div>',
            unsafe_allow_html=True,
        )

    page = st.session_state["page"]

    if page == "Home":
        render_home(client, user_id, st.session_state["user"])
    elif page == "Goals":
        render_dashboard(client, user_id)
    elif page == "Gratitude":
        render_gratitude_archive(client, user_id)
    elif page == "Applications":
        render_job_hunt(client, user_id, initial_tab="Applications")
    elif page == "Profile":
        render_profile(client, user_id, st.session_state["user"])


if __name__ == "__main__":
    main()