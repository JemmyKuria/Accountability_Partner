"""
views/auth_view.py — Split-screen login.
Left: fixed full-height sage panel (rendered via CSS positioning).
Right: the form column, shifted to the right half by global CSS.
"""

import streamlit as st


def _set_session(client, resp):
    session = resp.session
    st.session_state["user"] = resp.user
    st.session_state["access_token"] = session.access_token
    st.session_state["refresh_token"] = session.refresh_token


def _left_panel_html():
    return """
    <div class="ap-auth-left-content">
        <div class="ap-auth-left-inner">
            <div class="ap-auth-tagline">Your goals.<br>Your progress.</div>
            <div class="ap-auth-blurb">
                Stay consistent, track your journey,<br>and build the life you want.
            </div>
            <div class="ap-auth-bullets">
                <div class="ap-auth-bullet">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                         stroke="#5E7E55" stroke-width="2.4"
                         stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12"/>
                    </svg>
                    Track job applications
                </div>
                <div class="ap-auth-bullet">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                         stroke="#5E7E55" stroke-width="2.4"
                         stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12"/>
                    </svg>
                    Set goals &amp; reminders
                </div>
                <div class="ap-auth-bullet">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                         stroke="#5E7E55" stroke-width="2.4"
                         stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12"/>
                    </svg>
                    Be your best self
                </div>
            </div>
        </div>
    </div>
    """


def render_auth(client):
    # Marker activates the auth-specific CSS.
    st.markdown('<div class="ap-auth-marker"></div>', unsafe_allow_html=True)

    # Fixed left panel — positioning handled by CSS, so it renders
    # independently of the block container.
    st.markdown(_left_panel_html(), unsafe_allow_html=True)

    # Form column — the block container is already shifted right by CSS.
    st.markdown('<div class="ap-auth-welcome">Welcome back</div>', unsafe_allow_html=True)
    st.markdown('<div class="ap-auth-sub">Sign in to continue your journey.</div>', unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["Sign In", "Sign Up"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input(
                "Email address",
                placeholder="you@example.com",
                key="login_email",
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password",
            )

            c1, c2 = st.columns([1, 1])
            with c1:
                st.checkbox("Remember me", key="remember")
            with c2:
                st.markdown(
                    '<div style="text-align:right;padding-top:8px;">'
                    '<a href="#" style="font-size:0.82rem;color:#5E7E55;">Forgot password?</a>'
                    '</div>',
                    unsafe_allow_html=True,
                )

            submitted = st.form_submit_button("Sign In", type="primary")
            if submitted:
                if not email or not password:
                    st.error("Enter your email and password.")
                else:
                    try:
                        resp = client.auth.sign_in_with_password(
                            {"email": email, "password": password}
                        )
                        _set_session(client, resp)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Could not sign in: {e}")

        st.markdown('<div class="ap-auth-or">or</div>', unsafe_allow_html=True)
        st.button("Continue with Google", use_container_width=True, key="google_btn")

    with tab_signup:
        with st.form("signup_form"):
            new_email = st.text_input(
                "Email address",
                placeholder="you@example.com",
                key="signup_email",
            )
            new_password = st.text_input(
                "Password",
                type="password",
                placeholder="At least 6 characters",
                key="signup_password",
            )
            confirm = st.text_input(
                "Confirm password",
                type="password",
                placeholder="Repeat your password",
                key="signup_confirm",
            )
            submitted = st.form_submit_button("Create Account", type="primary")

            if submitted:
                if not new_email or not new_password:
                    st.error("Fill in every field.")
                elif new_password != confirm:
                    st.error("Passwords don't match.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    try:
                        resp = client.auth.sign_up(
                            {"email": new_email, "password": new_password}
                        )
                        if resp.user and resp.session:
                            _set_session(client, resp)
                            st.rerun()
                        else:
                            st.success("Account created. Check your email to confirm.")
                    except Exception as e:
                        st.error(f"Could not create account: {e}")

    st.markdown(
        '<div class="ap-auth-bottom">Don\'t have an account? <a href="#">Sign up</a></div>',
        unsafe_allow_html=True,
    )