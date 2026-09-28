"""
views/style.py
--------------
Global design system — sage + cream, warm editorial.
"""

import streamlit as st


# --------------------------------------------------------------------------
# Design tokens
# --------------------------------------------------------------------------
BG          = "#FAF8F4"
BG_SIDEBAR  = "#F0F4EC"
BG_CARD     = "#FFFFFF"
BG_HOVER    = "#F5F3EE"
BG_ALT      = "#F7F5F0"

BORDER      = "#E8E5DC"
BORDER_SOFT = "#F0EDE5"

TEXT        = "#2A2A2A"
TEXT_MUTED  = "#6B6B6B"
TEXT_DIM    = "#9A9A9A"

SAGE        = "#7A9A6E"
SAGE_DARK   = "#5E7E55"
SAGE_LIGHT  = "#E5EDE0"
SAGE_GLOW   = "rgba(122, 154, 110, 0.20)"

MINT_BG,   MINT_FG   = "#E8F1E2", "#5A7A50"
LAV_BG,    LAV_FG    = "#EDE7F5", "#7A5FA5"
CREAM_BG,  CREAM_FG  = "#F7F0DD", "#A58535"
BLUSH_BG,  BLUSH_FG  = "#F5E2E2", "#A55555"

PILL_APPLIED_BG,   PILL_APPLIED_FG   = "#E0E8F0", "#4A6FA5"
PILL_PROGRESS_BG,  PILL_PROGRESS_FG  = "#F5EDD0", "#A58535"
PILL_INTERVIEW_BG, PILL_INTERVIEW_FG = "#EAE2F0", "#7A5FA5"
PILL_OFFER_BG,     PILL_OFFER_FG     = "#E0EDE0", "#4A7A4A"
PILL_REJECTED_BG,  PILL_REJECTED_FG  = "#F0DEDE", "#A54A4A"
PILL_DECLINED_BG,  PILL_DECLINED_FG  = "#E5E0E0", "#6A5A5A"


def leaf_svg(size=20, color="#A8BFA0"):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C8 6 4 9 4 14a8 8 0 0 0 16 0c0-5-4-8-8-12z" fill="{color}" opacity="0.9"/><path d="M12 6v14" stroke="#FFFFFF" stroke-width="0.8" opacity="0.4"/></svg>'''


def inject_custom_css():
    st.markdown(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=Caveat:wght@500;600&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )

    st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, sans-serif;
        color: {TEXT_MUTED};
        -webkit-font-smoothing: antialiased;
    }}

    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Fraunces', Georgia, serif !important;
        color: {TEXT} !important;
        font-weight: 600 !important;
        letter-spacing: -0.015em;
    }}

    .stApp {{ background: {BG}; }}

    .block-container {{
        padding: 2rem 2.5rem 4rem 2.5rem;
        max-width: 1400px;
    }}

        /* ============================================================
       CHROME
       ============================================================ */
        [data-testid="stDecoration"] {{ display: none !important; }}
        #MainMenu {{ visibility: hidden !important; }}
        footer {{ visibility: hidden !important; }}

        header[data-testid="stHeader"] {{
            background: transparent !important;
            height: 0 !important;
        }}

        [data-testid="stToolbar"] {{ display: none !important; }}

        /* Kill the sidebar collapse button — sidebar stays open */
        [data-testid="stSidebarCollapseButton"] {{ display: none !important; }}
        [data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}

    /* ============================================================
       AUTH — split screen
       ============================================================ */
    body:has(.ap-auth-marker) .stApp {{ background: {BG}; }}

    body:has(.ap-auth-marker) .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 50%;
        height: 100vh;
        background: linear-gradient(150deg, #E8F0E2 0%, #D4E3CB 100%);
        z-index: 0;
        pointer-events: none;
    }}

    body:has(.ap-auth-marker) .stApp::after {{
        content: '';
        position: fixed;
        top: -120px;
        left: -80px;
        width: 560px;
        height: 560px;
        border-radius: 50%;
        background: {SAGE};
        opacity: 0.10;
        z-index: 0;
        pointer-events: none;
    }}

    body:has(.ap-auth-marker) .block-container {{
        max-width: 50% !important;
        margin-left: 50% !important;
        padding: 5rem 4rem !important;
        position: relative;
        z-index: 2;
    }}

    body:has(.ap-auth-marker) section[data-testid="stSidebar"] {{
        display: none !important;
    }}

    body:has(.ap-auth-marker) [data-testid="stSidebarCollapsedControl"],
    body:has(.ap-auth-marker) [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
    }}

    .ap-auth-left-content {{
        position: fixed;
        top: 0;
        left: 0;
        width: 50%;
        height: 100vh;
        padding: 4rem 3.5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        z-index: 1;
        pointer-events: none;
    }}

    .ap-auth-left-inner {{ max-width: 420px; }}

    .ap-auth-tagline {{
        font-family: 'Fraunces', serif;
        font-size: 3rem;
        font-weight: 600;
        color: {SAGE_DARK};
        line-height: 1.12;
        letter-spacing: -0.02em;
        margin-bottom: 1.25rem;
    }}

    .ap-auth-blurb {{
        color: #4A6B42;
        font-size: 1rem;
        line-height: 1.65;
        margin-bottom: 2.5rem;
        opacity: 0.9;
    }}

    .ap-auth-bullets {{
        display: flex;
        flex-direction: column;
        gap: 16px;
    }}

    .ap-auth-bullet {{
        display: flex;
        align-items: center;
        gap: 12px;
        color: {SAGE_DARK};
        font-size: 0.95rem;
        font-weight: 500;
    }}

    .ap-auth-bullet svg {{ flex-shrink: 0; }}

    .ap-auth-welcome {{
        font-family: 'Fraunces', serif;
        font-size: 2.2rem;
        font-weight: 600;
        color: {TEXT};
        margin-bottom: 0.4rem;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }}

    .ap-auth-sub {{
        color: {TEXT_MUTED};
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }}

    .ap-auth-or {{
        display: flex;
        align-items: center;
        gap: 14px;
        margin: 1.5rem 0;
        color: {TEXT_DIM};
        font-size: 0.8rem;
    }}

    .ap-auth-or::before,
    .ap-auth-or::after {{
        content: '';
        flex: 1;
        height: 1px;
        background: {BORDER};
    }}

    .ap-auth-bottom {{
        text-align: center;
        margin-top: 2rem;
        color: {TEXT_MUTED};
        font-size: 0.88rem;
    }}

    .ap-auth-bottom a {{
        color: {SAGE_DARK};
        font-weight: 600;
    }}

    /* ============================================================
       SIDEBAR
       ============================================================ */
    section[data-testid="stSidebar"] {{
        background: {BG_SIDEBAR} !important;
        border-right: 1px solid {BORDER};
        position: relative;
        overflow: hidden;
    }}

    section[data-testid="stSidebar"]::after {{
        content: '';
        position: absolute;
        bottom: -80px;
        left: -80px;
        width: 260px;
        height: 260px;
        background-image:
            radial-gradient(circle at 30% 30%, rgba(122,154,110,0.16) 0%, transparent 60%),
            radial-gradient(circle at 70% 70%, rgba(122,154,110,0.10) 0%, transparent 55%);
        pointer-events: none;
        z-index: 0;
    }}

    section[data-testid="stSidebar"] > div:first-child {{
        padding: 1.75rem 1rem;
        position: relative;
        z-index: 1;
    }}

    .ap-brand {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 4px 6px 22px 6px;
        margin-bottom: 18px;
        border-bottom: 1px solid rgba(122, 154, 110, 0.15);
    }}

    .ap-brand-mark {{
        width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}

    .ap-brand-text {{ display: flex; flex-direction: column; line-height: 1.15; }}

    .ap-brand-name {{
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 1.05rem;
        color: {TEXT};
        letter-spacing: -0.01em;
    }}

    .ap-brand-sub {{
        font-size: 0.66rem;
        color: {TEXT_DIM};
        letter-spacing: 0.14em;
        margin-top: 3px;
        text-transform: uppercase;
    }}

    /* ---- Sidebar nav buttons ---- */
    section[data-testid="stSidebar"] .stButton {{
        margin: 0 0 2px 0 !important;
        padding: 0 !important;
    }}

    section[data-testid="stSidebar"] .stButton > button {{
        background: transparent !important;
        color: {TEXT_MUTED} !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 11px 14px !important;
        min-height: 44px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        box-shadow: none !important;
        transition: background 0.15s ease, color 0.15s ease !important;
        width: 100% !important;
    }}

    section[data-testid="stSidebar"] .stButton > button > div {{
        gap: 12px !important;
        justify-content: flex-start !important;
    }}

    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(122, 154, 110, 0.08) !important;
        color: {TEXT} !important;
    }}

    section[data-testid="stSidebar"] .stButton > button[kind="primary"],
    section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {{
        background: #D8E5D0 !important;
        color: #2F4A28 !important;
        font-weight: 600 !important;
    }}

    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover,
    section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"]:hover {{
        background: #C9DBBE !important;
        color: #2F4A28 !important;
    }}

    section[data-testid="stSidebar"] .stButton > button [data-testid="stIconMaterial"] {{
        font-size: 1.15rem !important;
        color: inherit !important;
        margin: 0 !important;
    }}

    .ap-side-quote {{
        margin-top: 34px;
        padding: 20px 16px 12px 16px;
        font-family: 'Caveat', cursive;
        font-size: 1.15rem;
        color: {SAGE_DARK};
        line-height: 1.4;
        opacity: 0.75;
        border-top: 1px solid rgba(122, 154, 110, 0.15);
    }}

    /* ============================================================
       TYPOGRAPHY
       ============================================================ */
    .ap-page-title {{
        font-family: 'Fraunces', serif;
        font-size: 2rem;
        font-weight: 600;
        color: {TEXT};
        letter-spacing: -0.02em;
        margin: 0 0 0.3rem 0;
        line-height: 1.15;
    }}

    .ap-page-title .ap-leaf-inline {{
        display: inline-block;
        margin-left: 10px;
        vertical-align: middle;
    }}

    .ap-page-sub {{
        color: {TEXT_MUTED};
        font-size: 0.95rem;
        margin-bottom: 1.75rem;
        line-height: 1.5;
        max-width: 720px;
    }}

    .ap-greeting {{
        font-family: 'Fraunces', serif;
        font-size: 2rem;
        font-weight: 600;
        color: {TEXT};
        letter-spacing: -0.02em;
        margin-bottom: 0.25rem;
    }}

    .ap-greeting-sub {{
        font-family: 'Caveat', cursive;
        font-size: 1.15rem;
        color: {SAGE_DARK};
        opacity: 0.85;
        margin-bottom: 1.5rem;
    }}

    .ap-section-label {{
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        color: {TEXT_DIM};
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin: 1.5rem 0 0.75rem 0;
    }}

    /* ============================================================
       BUTTONS (main content)
       ============================================================ */
    .stButton > button,
    .stFormSubmitButton > button,
    .stDownloadButton > button {{
        background: {BG_CARD} !important;
        color: {TEXT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 0.55rem 1.1rem !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
    }}

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {{
        border-color: {SAGE} !important;
        color: {SAGE_DARK} !important;
        background: {BG_HOVER} !important;
    }}

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"],
    .stFormSubmitButton > button[data-testid="baseButton-primary"] {{
        background: {SAGE} !important;
        color: #FFFFFF !important;
        border: 1px solid {SAGE} !important;
        font-weight: 600 !important;
    }}

    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button[kind="primary"]:hover {{
        background: {SAGE_DARK} !important;
        border-color: {SAGE_DARK} !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 16px {SAGE_GLOW} !important;
    }}

    .stFormSubmitButton > button,
    .stButton > button[kind="primary"] {{ width: 100%; }}

    /* ============================================================
       INPUTS
       ============================================================ */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    .stDateInput input,
    .stSelectbox [data-baseweb="select"] > div,
    .stMultiSelect [data-baseweb="select"] > div {{
        background: {BG_CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 10px !important;
        color: {TEXT} !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.92rem !important;
        transition: border 0.15s ease, box-shadow 0.15s ease;
    }}

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {{ color: {TEXT_DIM} !important; }}

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {{
        border-color: {SAGE} !important;
        box-shadow: 0 0 0 3px {SAGE_GLOW} !important;
        outline: none !important;
    }}

    .stTextInput label, .stTextArea label, .stNumberInput label,
    .stDateInput label, .stSelectbox label, .stMultiSelect label,
    .stCheckbox label, .stRadio label, .stFileUploader label {{
        color: {TEXT_MUTED} !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }}

    [data-testid="stFileUploader"] section {{
        background: {BG_CARD} !important;
        border: 1px dashed {BORDER} !important;
        border-radius: 10px !important;
    }}

    [data-testid="stFileUploader"] section:hover {{ border-color: {SAGE} !important; }}

    .stSlider [data-baseweb="slider"] [role="slider"] {{
        background: {SAGE} !important;
        border-color: {SAGE} !important;
        box-shadow: 0 0 0 4px {SAGE_GLOW} !important;
    }}

    .stSlider [data-baseweb="slider"] > div > div {{ background: {SAGE} !important; }}

    /* ============================================================
       TABS
       ============================================================ */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        background: transparent;
        border-bottom: 1px solid {BORDER};
        padding: 0;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        color: {TEXT_MUTED} !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 12px 18px !important;
    }}

    .stTabs [data-baseweb="tab"]:hover {{ color: {TEXT} !important; }}
    .stTabs [aria-selected="true"] {{ color: {SAGE_DARK} !important; font-weight: 600 !important; }}
    .stTabs [data-baseweb="tab-highlight"] {{ background: {SAGE} !important; height: 2px !important; }}
    .stTabs [data-baseweb="tab-border"] {{ display: none !important; }}

    /* ============================================================
       EXPANDER
       ============================================================ */
    div[data-testid="stExpander"] {{
        background: {BG_CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }}

    div[data-testid="stExpander"] summary {{
        color: {TEXT_MUTED} !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 10px 14px !important;
    }}

    div[data-testid="stExpander"] summary:hover {{ color: {SAGE_DARK} !important; }}

    /* ============================================================
       ALERTS
       ============================================================ */
    div[data-testid="stAlert"] {{
        border-radius: 10px !important;
        border: 1px solid {BORDER} !important;
        background: {BG_CARD} !important;
        color: {TEXT_MUTED} !important;
    }}

    div[data-testid="stDataFrame"],
    div[data-testid="stDataEditor"] {{
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
        overflow: hidden;
    }}

    .stProgress > div > div > div > div {{ background: {SAGE} !important; }}

    hr {{ border: none; border-top: 1px solid {BORDER}; margin: 1.5rem 0; }}

    .stCaption, [data-testid="stCaptionContainer"] {{
        color: {TEXT_DIM} !important;
        font-size: 0.8rem !important;
    }}

    a {{ color: {SAGE_DARK}; text-decoration: none; }}
    a:hover {{ color: {SAGE}; }}

    /* ============================================================
       KPI
       ============================================================ */
    .ap-kpi {{
        background: {BG_CARD};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        min-height: 118px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: border-color 0.15s ease, transform 0.15s ease;
    }}

    .ap-kpi:hover {{ border-color: {SAGE}; transform: translateY(-2px); }}

    .ap-kpi-head {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 14px;
    }}

    .ap-kpi-icon {{
        width: 30px; height: 30px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}

    .ap-kpi-label {{
        font-size: 0.68rem;
        font-weight: 700;
        color: {TEXT_DIM};
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }}

    .ap-kpi-value {{
        font-family: 'Fraunces', serif;
        font-size: 2.1rem;
        font-weight: 600;
        color: {TEXT};
        line-height: 1;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }}

    .ap-kpi-foot {{ color: {TEXT_DIM}; font-size: 0.75rem; }}

    .ap-kpi-watermark {{
        position: absolute;
        bottom: -8px;
        right: -8px;
        opacity: 0.18;
        pointer-events: none;
    }}

    /* ============================================================
       ACTIVITY LIST
       ============================================================ */
    .ap-activity-item {{
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 14px 0;
        border-bottom: 1px solid {BORDER_SOFT};
    }}

    .ap-activity-item:last-child {{ border-bottom: none; }}

    .ap-activity-icon {{
        width: 34px; height: 34px;
        border-radius: 9px;
        background: {SAGE_LIGHT};
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}

    .ap-activity-text {{ flex: 1; color: {TEXT}; font-size: 0.88rem; }}
    .ap-activity-time {{ color: {TEXT_DIM}; font-size: 0.75rem; white-space: nowrap; }}

    /* ============================================================
       QUOTE CARD
       ============================================================ */
    .ap-quote-card {{
        background: linear-gradient(160deg, {SAGE_LIGHT} 0%, #DCE8D4 100%);
        border: 1px solid #D0DEC7;
        border-radius: 14px;
        padding: 28px 24px;
        position: relative;
        overflow: hidden;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .ap-quote-card::after {{
        content: '';
        position: absolute;
        bottom: -40px; right: -40px;
        width: 140px; height: 140px;
        border-radius: 50%;
        background: {SAGE};
        opacity: 0.10;
    }}

    .ap-quote-text {{
        font-family: 'Fraunces', serif;
        font-size: 1.05rem;
        font-style: italic;
        color: {SAGE_DARK};
        line-height: 1.5;
        position: relative;
        z-index: 1;
    }}

    .ap-quote-mark {{
        font-family: 'Fraunces', serif;
        font-size: 2.5rem;
        color: {SAGE};
        line-height: 1;
        margin-bottom: 6px;
        opacity: 0.5;
    }}

    /* ============================================================
       TABLES
       ============================================================ */
    .ap-table-wrap {{
        background: {BG_CARD};
        border: 1px solid {BORDER};
        border-radius: 14px;
        overflow: hidden;
    }}

    .ap-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
    }}

    .ap-table thead th {{
        background: {BG_ALT};
        color: {TEXT_MUTED};
        font-weight: 600;
        font-size: 0.72rem;
        text-align: left;
        padding: 12px 14px;
        border-bottom: 1px solid {BORDER};
        letter-spacing: 0.03em;
        text-transform: uppercase;
        white-space: nowrap;
    }}

    .ap-table tbody td {{
        padding: 14px;
        border-bottom: 1px solid {BORDER_SOFT};
        color: {TEXT};
        vertical-align: middle;
    }}

    .ap-table tbody tr:last-child td {{ border-bottom: none; }}
    .ap-table tbody tr:hover {{ background: {BG_HOVER}; }}

    .ap-table .ap-cell-num {{ color: {TEXT_DIM}; font-weight: 500; }}
    .ap-table .ap-cell-pos {{ font-weight: 600; color: {TEXT}; }}
    .ap-table .ap-cell-company {{ color: {TEXT_MUTED}; }}
    .ap-table .ap-cell-notes {{ color: {TEXT_MUTED}; font-size: 0.8rem; }}

    /* ============================================================
       STATUS PILLS (applications)
       ============================================================ */
    .ap-pill {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        white-space: nowrap;
    }}

    .ap-pill-applied   {{ background: {PILL_APPLIED_BG};   color: {PILL_APPLIED_FG}; }}
    .ap-pill-progress  {{ background: {PILL_PROGRESS_BG};  color: {PILL_PROGRESS_FG}; }}
    .ap-pill-interview {{ background: {PILL_INTERVIEW_BG}; color: {PILL_INTERVIEW_FG}; }}
    .ap-pill-offer     {{ background: {PILL_OFFER_BG};     color: {PILL_OFFER_FG}; }}
    .ap-pill-rejected  {{ background: {PILL_REJECTED_BG};  color: {PILL_REJECTED_FG}; }}
    .ap-pill-declined  {{ background: {PILL_DECLINED_BG};  color: {PILL_DECLINED_FG}; }}

    /* ============================================================
       JOB LISTING ROW
       ============================================================ */
    .ap-job-row {{
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px 18px;
        background: {BG_CARD};
        border: 1px solid {BORDER};
        border-radius: 12px;
        margin-bottom: 10px;
        transition: border-color 0.15s ease;
    }}

    .ap-job-row:hover {{ border-color: {SAGE}; }}

    .ap-job-logo {{
        width: 42px; height: 42px;
        border-radius: 10px;
        background: {BG_ALT};
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Fraunces', serif;
        font-weight: 700;
        color: {SAGE_DARK};
        font-size: 0.95rem;
        flex-shrink: 0;
    }}

    .ap-job-body {{ flex: 1; min-width: 0; }}
    .ap-job-title {{
        font-weight: 600;
        color: {TEXT};
        font-size: 0.95rem;
        margin-bottom: 3px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .ap-job-company {{ color: {TEXT_MUTED}; font-size: 0.82rem; }}
    .ap-job-badge {{
        font-size: 0.65rem;
        font-weight: 700;
        color: {SAGE_DARK};
        background: {SAGE_LIGHT};
        padding: 2px 8px;
        border-radius: 50px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}

    /* ============================================================
       TAGS
       ============================================================ */
    .ap-tag {{
        display: inline-block;
        background: {SAGE_LIGHT};
        color: {SAGE_DARK};
        font-size: 0.68rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 50px;
        letter-spacing: 0.03em;
    }}

    /* ============================================================
       GRATITUDE ENTRY
       ============================================================ */
    .ap-gratitude-entry {{
        background: {BG_CARD};
        border: 1px solid {BORDER};
        border-left: 3px solid {SAGE};
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }}

    .ap-gratitude-date {{
        font-size: 0.68rem;
        font-weight: 600;
        color: {TEXT_DIM};
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }}

    .ap-gratitude-content {{
        color: {TEXT};
        font-size: 0.95rem;
        line-height: 1.5;
    }}

    /* ============================================================
       GOALS PAGE — pastel KPIs
       ============================================================ */
    .ap-kpi-pastel {{
        border: none;
        border-radius: 14px;
        padding: 18px 20px;
        display: flex;
        align-items: center;
        gap: 14px;
        min-height: 88px;
        transition: transform 0.15s ease;
    }}

    .ap-kpi-pastel:hover {{ transform: translateY(-2px); }}

    .ap-kpi-pastel-icon {{
        width: 40px; height: 40px;
        border-radius: 10px;
        background: rgba(255,255,255,0.75);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}

    .ap-kpi-pastel-body {{ flex: 1; min-width: 0; }}

    .ap-kpi-pastel-label {{
        font-size: 0.75rem;
        font-weight: 500;
        color: #6B6B6B;
        margin-bottom: 4px;
        letter-spacing: 0.01em;
    }}

    .ap-kpi-pastel-value {{
        font-family: 'Fraunces', serif;
        font-size: 1.85rem;
        font-weight: 600;
        color: #2A2A2A;
        line-height: 1;
        letter-spacing: -0.02em;
    }}

    /* Goal type pills */
    .ap-type-financial    {{ background: #EDE7F5; color: #7A5FA5; }}
    .ap-type-health       {{ background: #E0E8F0; color: #4A6FA5; }}
    .ap-type-learning     {{ background: #E0E8F0; color: #4A6FA5; }}
    .ap-type-career       {{ background: #EAE2F0; color: #7A5FA5; }}
    .ap-type-personal     {{ background: #F7F0DD; color: #A58535; }}
    .ap-type-relationship {{ background: #F5E2E2; color: #A55555; }}
    .ap-type-project      {{ background: #E0E8F0; color: #4A6FA5; }}
    .ap-type-default      {{ background: #EDEDED; color: #6A6A6A; }}

    /* Priority pills */
    .ap-priority-high     {{ background: #F5E2E2; color: #A55555; }}
    .ap-priority-medium   {{ background: #F7F0DD; color: #A58535; }}
    .ap-priority-low      {{ background: #E0E8F0; color: #4A6FA5; }}

    /* Goal status pills */
    .ap-status-done        {{ background: #E0EDE0; color: #4A7A4A; }}
    .ap-status-in-progress {{ background: #F5EDD0; color: #A58535; }}
    .ap-status-not-started {{ background: #EDEDED; color: #6A6A6A; }}

    /* Goals table */
    .ap-goals-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.87rem;
    }}

    .ap-goals-table thead th {{
        background: {BG_ALT};
        color: {TEXT_MUTED};
        font-weight: 600;
        font-size: 0.7rem;
        text-align: left;
        padding: 12px 14px;
        border-bottom: 1px solid {BORDER};
        letter-spacing: 0.06em;
        text-transform: uppercase;
        white-space: nowrap;
    }}

    .ap-goals-table tbody td {{
        padding: 16px 14px;
        border-bottom: 1px solid {BORDER_SOFT};
        color: {TEXT};
        vertical-align: middle;
    }}

    .ap-goals-table tbody tr:last-child td {{ border-bottom: none; }}
    .ap-goals-table tbody tr:hover {{ background: {BG_HOVER}; }}

    .ap-goal-title-cell {{
        font-weight: 600;
        color: {TEXT};
        font-size: 0.92rem;
        line-height: 1.3;
    }}

    .ap-goal-desc {{
        color: {TEXT_DIM};
        font-size: 0.78rem;
        margin-top: 2px;
    }}

    .ap-pill-sm {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        white-space: nowrap;
    }}

    /* ============================================================
       GRATITUDE TYPE PILLS
       ============================================================ */
    .ap-gtype-personal     {{ background: #F7F0DD; color: #A58535; }}
    .ap-gtype-relationship {{ background: #F5E2E2; color: #A55555; }}
    .ap-gtype-career       {{ background: #EAE2F0; color: #7A5FA5; }}
    .ap-gtype-health       {{ background: #E8F1E2; color: #5A7A50; }}
    .ap-gtype-travel       {{ background: #E0E8F0; color: #4A6FA5; }}
    .ap-gtype-opportunity  {{ background: #EDE7F5; color: #7A5FA5; }}
    .ap-gtype-small-win    {{ background: #E0EDE0; color: #4A7A4A; }}

    /* ============================================================
       HOME PAGE
       ============================================================ */
    .ap-home-top {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 22px;
        gap: 20px;
        flex-wrap: wrap;
    }}

    .ap-home-top-right {{
        display: flex;
        align-items: center;
        gap: 14px;
        padding-top: 8px;
    }}

    .ap-date-chip {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: {BG_CARD};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 8px 14px;
        color: {TEXT_MUTED};
        font-size: 0.82rem;
        font-weight: 500;
    }}

    .ap-avatar {{
        width: 40px; height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, {SAGE} 0%, {SAGE_DARK} 100%);
        color: #FFFFFF;
        font-family: 'Fraunces', serif;
        font-weight: 700;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .ap-hero {{
        background: linear-gradient(120deg, #E8F0E2 0%, #DCE8D4 55%, #C9DDBE 100%);
        border: 1px solid #D0DEC7;
        border-radius: 16px;
        padding: 32px 36px;
        position: relative;
        overflow: hidden;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 22px;
    }}

    .ap-hero::before {{
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 240px; height: 240px;
        border-radius: 50%;
        background: {SAGE};
        opacity: 0.15;
    }}

    .ap-hero::after {{
        content: '';
        position: absolute;
        bottom: -80px; right: 120px;
        width: 180px; height: 180px;
        border-radius: 50%;
        background: #FFFFFF;
        opacity: 0.35;
    }}

    .ap-hero-inner {{ position: relative; z-index: 1; max-width: 520px; }}

    .ap-hero-title {{
        font-family: 'Fraunces', serif;
        font-size: 1.7rem;
        font-weight: 600;
        color: {SAGE_DARK};
        letter-spacing: -0.02em;
        margin-bottom: 8px;
        line-height: 1.15;
    }}

    .ap-hero-sub {{
        color: #4A6B42;
        font-size: 0.92rem;
        line-height: 1.55;
        opacity: 0.9;
        margin-bottom: 10px;
    }}

    .ap-home-kpi {{
        border-radius: 16px;
        padding: 20px 22px;
        position: relative;
        overflow: hidden;
        height: 170px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.15s ease;
    }}

    .ap-home-kpi:hover {{ transform: translateY(-2px); }}

    .ap-home-kpi-top {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 12px;
    }}

    .ap-home-kpi-icon {{
        width: 34px; height: 34px;
        border-radius: 10px;
        background: rgba(255,255,255,0.75);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}

    .ap-home-kpi-label {{
        font-family: 'Fraunces', serif;
        font-size: 1.05rem;
        font-weight: 600;
        color: {TEXT};
    }}

    .ap-home-kpi-value {{
        font-family: 'Fraunces', serif;
        font-size: 2.3rem;
        font-weight: 600;
        color: {TEXT};
        line-height: 1;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }}

    .ap-home-kpi-unit {{
        color: {TEXT_MUTED};
        font-size: 0.82rem;
        margin-bottom: 12px;
    }}

    .ap-home-kpi-foot {{
        font-size: 0.78rem;
        color: {TEXT_MUTED};
        line-height: 1.6;
    }}

    .ap-home-kpi-dot {{
        display: inline-block;
        width: 6px; height: 6px;
        border-radius: 50%;
        margin-right: 6px;
        vertical-align: middle;
    }}

    .ap-home-kpi-chevron {{
        position: absolute;
        right: 18px;
        top: 50%;
        transform: translateY(-50%);
        width: 30px; height: 30px;
        border-radius: 50%;
        background: rgba(255,255,255,0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        color: {SAGE_DARK};
    }}

    .ap-goal-row {{
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 14px 12px;
        border-bottom: 1px solid {BORDER_SOFT};
        transition: background 0.15s ease;
        border-radius: 8px;
    }}

    .ap-goal-row:hover {{ background: {BG_HOVER}; }}
    .ap-goal-row:last-child {{ border-bottom: none; }}

    .ap-goal-check {{
        width: 20px; height: 20px;
        border-radius: 6px;
        border: 1.5px solid {BORDER};
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .ap-goal-check.done {{
        background: {SAGE};
        border-color: {SAGE};
        color: white;
    }}

    .ap-goal-row-body {{ flex: 1; min-width: 0; }}
    .ap-goal-row-title {{ color: {TEXT}; font-size: 0.88rem; font-weight: 500; }}
    .ap-goal-row-meta {{ color: {TEXT_DIM}; font-size: 0.72rem; margin-top: 3px; }}

    .ap-upcoming-item {{
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 12px 0;
        border-bottom: 1px solid {BORDER_SOFT};
    }}

    .ap-upcoming-item:last-child {{ border-bottom: none; }}

    .ap-upcoming-date {{
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 44px;
        flex-shrink: 0;
    }}

    .ap-upcoming-date .d {{
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 1rem;
        color: {TEXT};
        line-height: 1;
    }}

    .ap-upcoming-date .m {{
        font-size: 0.68rem;
        font-weight: 600;
        color: {TEXT_DIM};
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 3px;
    }}

    .ap-upcoming-body {{ flex: 1; min-width: 0; }}
    .ap-upcoming-title {{ font-weight: 500; color: {TEXT}; font-size: 0.88rem; }}
    .ap-upcoming-sub {{ color: {TEXT_DIM}; font-size: 0.75rem; margin-top: 2px; }}

    .ap-recent-item {{
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px 0;
        border-bottom: 1px solid {BORDER_SOFT};
    }}

    .ap-recent-item:last-child {{ border-bottom: none; }}
    .ap-recent-date {{
        font-size: 0.68rem;
        font-weight: 600;
        color: {TEXT_DIM};
        letter-spacing: 0.06em;
        text-transform: uppercase;
        white-space: nowrap;
        padding-top: 3px;
        min-width: 64px;
    }}
    .ap-recent-body {{ flex: 1; min-width: 0; }}
    .ap-recent-text {{ color: {TEXT}; font-size: 0.85rem; line-height: 1.45; }}

    .ap-ring-row {{
        display: flex;
        justify-content: space-around;
        gap: 12px;
        flex-wrap: wrap;
    }}

    .ap-ring-item {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        min-width: 96px;
    }}

    .ap-ring-label {{
        font-size: 0.72rem;
        font-weight: 600;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}

    .ap-ring-value {{
        font-size: 0.72rem;
        color: {TEXT_DIM};
    }}

    .ap-section-head {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }}

    .ap-section-head-title {{
        font-family: 'Fraunces', serif;
        font-size: 1.15rem;
        font-weight: 600;
        color: {TEXT};
    }}

    .ap-section-head-link {{
        color: {SAGE_DARK};
        font-size: 0.78rem;
        font-weight: 500;
        text-decoration: none;
    }}

    /* ============================================================
       RESPONSIVE
       ============================================================ */
    @media (max-width: 1024px) {{
        .block-container {{ padding: 1.5rem; }}
        .ap-page-title {{ font-size: 1.7rem; }}
        .ap-auth-tagline {{ font-size: 2rem; }}
        .ap-hero {{ padding: 26px 24px; }}
        .ap-hero-title {{ font-size: 1.4rem; }}
    }}

    @media (max-width: 768px) {{
        .block-container {{
            padding: 1.25rem 1rem 3rem 1rem !important;
        }}

        body:has(.ap-auth-marker) .stApp::before,
        body:has(.ap-auth-marker) .stApp::after,
        .ap-auth-left-content {{ display: none !important; }}

        body:has(.ap-auth-marker) .block-container {{
            max-width: 100% !important;
            margin-left: 0 !important;
            padding: 3rem 1.25rem !important;
        }}

        .ap-page-title, .ap-greeting {{ font-size: 1.55rem; }}

        [data-testid="stHorizontalBlock"] {{
            flex-direction: column !important;
            gap: 0.75rem !important;
        }}
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
            width: 100% !important;
            flex: 1 1 auto !important;
            min-width: 0 !important;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            overflow-x: auto;
            flex-wrap: nowrap;
            -webkit-overflow-scrolling: touch;
        }}
        .stTabs [data-baseweb="tab"] {{
            padding: 10px 14px !important;
            font-size: 0.85rem !important;
            white-space: nowrap;
        }}

        .ap-kpi {{ padding: 14px 16px; min-height: auto; }}
        .ap-kpi-value {{ font-size: 1.7rem; }}
        .ap-kpi-pastel {{ padding: 14px 16px; min-height: auto; }}
        .ap-kpi-pastel-value {{ font-size: 1.5rem; }}

        .ap-table-wrap {{ overflow-x: auto; }}
        .ap-table {{ min-width: 700px; }}
        .ap-goals-table {{ min-width: 700px; }}

        .ap-job-row {{ flex-wrap: wrap; }}

        .ap-home-top {{ flex-direction: column; }}
        .ap-home-top-right {{ padding-top: 0; }}
        .ap-hero {{ padding: 24px 20px; min-height: auto; }}
        .ap-hero-title {{ font-size: 1.3rem; }}
        .ap-home-kpi {{ height: auto; min-height: 150px; padding: 16px 18px; }}
        .ap-home-kpi-value {{ font-size: 1.9rem; }}
        .ap-home-kpi-chevron {{ display: none; }}
    }}

    @media (max-width: 480px) {{
        .block-container {{ padding-left: 0.85rem !important; padding-right: 0.85rem !important; }}
        .ap-page-title, .ap-greeting {{ font-size: 1.35rem; }}
        .ap-kpi-value {{ font-size: 1.5rem; }}
        .ap-kpi-pastel-value {{ font-size: 1.35rem; }}
        .ap-home-kpi-value {{ font-size: 1.7rem; }}
    }}
    </style>
    """, unsafe_allow_html=True)