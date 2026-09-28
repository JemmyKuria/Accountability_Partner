"""views/profile.py — Profile page."""

import streamlit as st

from views.style import leaf_svg


def render_profile(client, user_id, user):
    st.markdown(
        f'<div class="ap-page-title">Profile <span class="ap-leaf-inline">{leaf_svg(18, "#7A9A6E")}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="ap-page-sub">Manage your account and personal details.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])

    with c1:
        with st.container(border=True):
            initials = (user.email or "AP")[:2].upper()
            st.markdown(
                f"""
                <div style="text-align:center;padding:16px 0;">
                    <div style="width:72px;height:72px;border-radius:50%;background:#E5EDE0;
                                display:inline-flex;align-items:center;justify-content:center;
                                font-family:Fraunces,serif;font-weight:700;font-size:1.5rem;color:#5E7E55;">
                        {initials}
                    </div>
                    <div style="font-family:Fraunces,serif;font-size:1.2rem;font-weight:600;
                                color:#2A2A2A;margin-top:12px;">{user.email.split("@")[0].title()}</div>
                    <div style="color:#9A9A9A;font-size:0.82rem;margin-top:4px;">{user.email}</div>
                    <div style="font-family:Caveat,cursive;color:#5E7E55;font-size:1.05rem;
                                margin-top:16px;">More opportunities.<br>More growth.<br>Same you, just stronger.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with c2:
        with st.container(border=True):
            st.markdown('<div class="ap-section-label">Personal Information</div>', unsafe_allow_html=True)
            st.text_input("Full Name", value=user.email.split("@")[0].title(), key="p_name")
            st.text_input("Email", value=user.email, disabled=True, key="p_email")

            st.markdown('<div class="ap-section-label">Account Settings</div>', unsafe_allow_html=True)
            if st.button("Change Password", use_container_width=True, key="p_pw"):
                try:
                    client.auth.reset_password_email(user.email)
                    st.success("Password reset email sent.")
                except Exception as e:
                    st.error(f"Could not send reset: {e}")
            if st.button("Log Out", use_container_width=True, key="p_lo"):
                client.auth.sign_out()
                for k in ("user", "access_token", "refresh_token"):
                    st.session_state.pop(k, None)
                st.rerun()