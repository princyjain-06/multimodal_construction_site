"""
Custom CSS styles for the Multimodal Construction Intelligence Platform.
Dark-mode construction theme with amber/gold accent palette.
"""

import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        /* ── Google Font ── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        /* ── Root Variables ── */
        :root {
            --amber:   #F59E0B;
            --amber-d: #B45309;
            --amber-l: #FCD34D;
            --slate-900: #0F172A;
            --slate-800: #1E293B;
            --slate-700: #334155;
            --slate-600: #475569;
            --slate-400: #94A3B8;
            --slate-200: #E2E8F0;
            --slate-100: #F1F5F9;
            --green:  #10B981;
            --red:    #EF4444;
            --orange: #F97316;
            --blue:   #3B82F6;
            --purple: #8B5CF6;
            --radius: 14px;
            --shadow: 0 4px 24px rgba(0,0,0,.45);
        }

        /* ── Global ── */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }
        .main { background: var(--slate-900); }
        .stApp { background: var(--slate-900); }
        section[data-testid="stSidebar"] {
            background: var(--slate-800) !important;
            border-right: 1px solid var(--slate-700);
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: var(--slate-800); }
        ::-webkit-scrollbar-thumb { background: var(--slate-600); border-radius: 4px; }

        /* ── Main Header ── */
        .main-header {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 60%, #1a1033 100%);
            border: 1px solid var(--slate-700);
            border-radius: var(--radius);
            padding: 2rem 2.5rem;
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow);
        }
        .main-header::before {
            content: "";
            position: absolute;
            top: -40%;
            right: -10%;
            width: 400px; height: 400px;
            background: radial-gradient(circle, rgba(245,158,11,.15) 0%, transparent 70%);
            pointer-events: none;
        }
        .header-badge {
            display: inline-block;
            background: linear-gradient(90deg, var(--amber), var(--amber-l));
            color: var(--slate-900);
            font-size: .65rem;
            font-weight: 700;
            letter-spacing: .12em;
            padding: 3px 12px;
            border-radius: 99px;
            margin-bottom: .75rem;
        }
        .header-title {
            font-size: 2rem;
            font-weight: 800;
            color: var(--slate-100);
            margin: 0 0 .4rem;
            line-height: 1.2;
        }
        .header-subtitle {
            color: var(--slate-400);
            font-size: .9rem;
            margin: 0;
        }

        /* ── Demo Banner ── */
        .demo-banner {
            background: linear-gradient(90deg, rgba(245,158,11,.15), rgba(251,191,36,.1));
            border: 1px solid rgba(245,158,11,.4);
            border-radius: 10px;
            padding: .75rem 1.25rem;
            color: var(--amber-l);
            font-size: .88rem;
            margin-bottom: 1.25rem;
        }

        /* ── Card ── */
        .card {
            background: var(--slate-800);
            border: 1px solid var(--slate-700);
            border-radius: var(--radius);
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: var(--shadow);
            transition: border-color .2s;
        }
        .card:hover { border-color: var(--slate-600); }
        .card-title {
            font-size: .75rem;
            font-weight: 600;
            letter-spacing: .1em;
            text-transform: uppercase;
            color: var(--slate-400);
            margin-bottom: .3rem;
        }
        .card-value {
            font-size: 2rem;
            font-weight: 800;
            color: var(--slate-100);
            line-height: 1.1;
        }
        .card-sub {
            font-size: .75rem;
            color: var(--slate-400);
            margin-top: .25rem;
        }

        /* ── Status Pills ── */
        .pill {
            display: inline-block;
            padding: 3px 14px;
            border-radius: 99px;
            font-size: .78rem;
            font-weight: 600;
            letter-spacing: .04em;
        }
        .pill-green  { background: rgba(16,185,129,.2); color: #34D399; border: 1px solid rgba(16,185,129,.35); }
        .pill-amber  { background: rgba(245,158,11,.2);  color: var(--amber-l); border: 1px solid rgba(245,158,11,.35); }
        .pill-orange { background: rgba(249,115,22,.2);  color: #FB923C; border: 1px solid rgba(249,115,22,.35); }
        .pill-red    { background: rgba(239,68,68,.2);   color: #F87171; border: 1px solid rgba(239,68,68,.35); }
        .pill-blue   { background: rgba(59,130,246,.2);  color: #60A5FA; border: 1px solid rgba(59,130,246,.35); }
        .pill-purple { background: rgba(139,92,246,.2);  color: #A78BFA; border: 1px solid rgba(139,92,246,.35); }

        /* ── Section Headers ── */
        .section-header {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--slate-100);
            padding-bottom: .5rem;
            border-bottom: 2px solid var(--amber);
            margin: 1.5rem 0 1rem;
            display: flex;
            align-items: center;
            gap: .5rem;
        }

        /* ── Hazard Items ── */
        .hazard-item {
            background: var(--slate-800);
            border-left: 4px solid var(--red);
            border-radius: 0 10px 10px 0;
            padding: .85rem 1.1rem;
            margin-bottom: .65rem;
        }
        .hazard-item.medium { border-left-color: var(--orange); }
        .hazard-item.low    { border-left-color: var(--amber); }
        .hazard-item.critical { border-left-color: #DC2626; background: rgba(220,38,38,.08); }
        .hazard-title { font-weight: 600; color: var(--slate-100); font-size: .9rem; }
        .hazard-remedy { color: var(--slate-400); font-size: .82rem; margin-top: .2rem; }

        /* ── PPE Checklist ── */
        .ppe-item {
            display: flex;
            align-items: center;
            gap: .65rem;
            padding: .55rem .9rem;
            border-radius: 8px;
            background: var(--slate-800);
            border: 1px solid var(--slate-700);
            margin-bottom: .4rem;
            font-size: .88rem;
            color: var(--slate-200);
        }
        .ppe-ok  { border-left: 3px solid var(--green); }
        .ppe-ng  { border-left: 3px solid var(--red); }
        .ppe-na  { border-left: 3px solid var(--slate-600); }

        /* ── Score Ring ── */
        .score-ring-wrap {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: .3rem;
            padding: 1.5rem;
        }
        .score-ring-num {
            font-size: 3.5rem;
            font-weight: 800;
            line-height: 1;
        }
        .score-ring-label {
            font-size: .75rem;
            color: var(--slate-400);
            text-transform: uppercase;
            letter-spacing: .1em;
        }

        /* ── Progress Bar ── */
        .progress-wrap {
            background: var(--slate-700);
            border-radius: 99px;
            height: 10px;
            overflow: hidden;
            margin: .4rem 0;
        }
        .progress-fill {
            height: 100%;
            border-radius: 99px;
            background: linear-gradient(90deg, var(--amber), var(--amber-l));
            transition: width .5s ease;
        }

        /* ── Chat Bubbles ── */
        .chat-user {
            background: linear-gradient(135deg, rgba(245,158,11,.25), rgba(245,158,11,.12));
            border: 1px solid rgba(245,158,11,.3);
            border-radius: 16px 16px 4px 16px;
            padding: .85rem 1.1rem;
            margin: .5rem 0;
            margin-left: 15%;
            color: var(--slate-100);
            font-size: .88rem;
        }
        .chat-assistant {
            background: var(--slate-800);
            border: 1px solid var(--slate-700);
            border-radius: 16px 16px 16px 4px;
            padding: .85rem 1.1rem;
            margin: .5rem 0;
            margin-right: 10%;
            color: var(--slate-200);
            font-size: .88rem;
        }
        .chat-label {
            font-size: .7rem;
            font-weight: 600;
            letter-spacing: .08em;
            text-transform: uppercase;
            margin-bottom: .3rem;
        }
        .chat-label-user { color: var(--amber); }
        .chat-label-ai   { color: var(--blue); }

        /* ── Weather Alert ── */
        .weather-alert {
            border-radius: var(--radius);
            padding: 1.2rem 1.5rem;
            margin-bottom: .75rem;
            border: 1px solid;
        }
        .weather-alert.critical {
            background: rgba(220,38,38,.12);
            border-color: rgba(220,38,38,.4);
            color: #FCA5A5;
        }
        .weather-alert.warning {
            background: rgba(249,115,22,.12);
            border-color: rgba(249,115,22,.4);
            color: #FDBA74;
        }
        .weather-alert.info {
            background: rgba(59,130,246,.12);
            border-color: rgba(59,130,246,.4);
            color: #93C5FD;
        }
        .weather-alert.safe {
            background: rgba(16,185,129,.12);
            border-color: rgba(16,185,129,.4);
            color: #6EE7B7;
        }
        .weather-alert-title {
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: .4rem;
            display: flex;
            align-items: center;
            gap: .5rem;
        }
        .weather-alert-body { font-size: .85rem; line-height: 1.6; }

        /* ── Tabs override ── */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--slate-800);
            border-radius: 12px;
            padding: 4px;
            gap: 4px;
            border: 1px solid var(--slate-700);
        }
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: var(--slate-400);
            border-radius: 8px;
            font-weight: 500;
            font-size: .85rem;
            padding: .4rem .9rem;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--amber), var(--amber-d)) !important;
            color: var(--slate-900) !important;
            font-weight: 700;
        }
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 1.5rem;
        }

        /* ── Buttons ── */
        .stButton > button {
            background: linear-gradient(135deg, var(--amber), var(--amber-d));
            color: var(--slate-900);
            font-weight: 700;
            border: none;
            border-radius: 10px;
            padding: .55rem 1.5rem;
            transition: transform .15s, box-shadow .15s;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(245,158,11,.35);
        }

        /* ── Metric override ── */
        [data-testid="stMetricValue"] {
            color: var(--amber-l) !important;
            font-weight: 800 !important;
        }
        [data-testid="stMetricLabel"] {
            color: var(--slate-400) !important;
            font-size: .8rem !important;
        }

        /* ── Sidebar Labels ── */
        .sidebar-logo {
            text-align: center;
            padding: 1rem 0 .5rem;
        }
        .sidebar-logo .logo-icon {
            font-size: 2.5rem;
        }
        .sidebar-logo .logo-title {
            font-size: 1rem;
            font-weight: 800;
            color: var(--amber-l);
            margin-top: .3rem;
        }
        .sidebar-logo .logo-sub {
            font-size: .7rem;
            color: var(--slate-400);
        }
        .arch-box {
            background: var(--slate-900);
            border: 1px solid var(--slate-700);
            border-radius: 10px;
            padding: .85rem 1rem;
            font-size: .77rem;
            color: var(--slate-400);
            line-height: 1.7;
        }
        .arch-box span { color: var(--amber-l); font-weight: 600; }

        /* ── Uploader ── */
        [data-testid="stFileUploader"] {
            background: var(--slate-800);
            border: 2px dashed var(--slate-600);
            border-radius: 12px;
            padding: 1rem;
            transition: border-color .2s;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: var(--amber);
        }

        /* ── Image viewer ── */
        [data-testid="stImage"] img {
            border-radius: 10px;
            border: 1px solid var(--slate-700);
        }

        /* ── Crack defect box ── */
        .defect-card {
            background: linear-gradient(135deg, rgba(30,41,59,1), rgba(15,23,42,1));
            border: 1px solid var(--slate-700);
            border-radius: var(--radius);
            padding: 1.5rem;
        }
        .defect-type {
            font-size: 1.3rem;
            font-weight: 800;
            color: var(--amber-l);
        }
        .defect-meta {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: .75rem;
            margin-top: 1rem;
        }
        .defect-meta-item {
            background: var(--slate-800);
            border-radius: 8px;
            padding: .6rem .8rem;
        }
        .defect-meta-label {
            font-size: .7rem;
            color: var(--slate-400);
            text-transform: uppercase;
            letter-spacing: .08em;
        }
        .defect-meta-value {
            font-size: .95rem;
            font-weight: 700;
            color: var(--slate-100);
            margin-top: .15rem;
        }

        /* ── 3D Render box ── */
        .render-box {
            border-radius: var(--radius);
            overflow: hidden;
            border: 1px solid var(--slate-700);
            position: relative;
        }
        .render-box img {
            width: 100%;
            display: block;
        }
        .render-overlay {
            position: absolute;
            bottom: 0; left: 0; right: 0;
            background: linear-gradient(transparent, rgba(0,0,0,.75));
            padding: 1rem;
            color: var(--slate-200);
            font-size: .8rem;
        }

        /* ── Divider ── */
        hr { border-color: var(--slate-700) !important; }

        /* ── JSON display ── */
        .json-display {
            font-family: 'JetBrains Mono', monospace;
            font-size: .77rem;
            background: #0a0f1e;
            border: 1px solid var(--slate-700);
            border-radius: 10px;
            padding: 1rem;
            overflow-x: auto;
            color: #7dd3fc;
        }

        /* ── Glow separator ── */
        .glow-sep {
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--amber), transparent);
            margin: 1.5rem 0;
            opacity: .5;
        }

        /* ── Spinner text ── */
        .spin-label {
            text-align: center;
            color: var(--amber-l);
            font-weight: 600;
            font-size: .9rem;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50%       { opacity: .5; }
        }

        /* ── INR value display ── */
        .inr-display {
            background: linear-gradient(135deg, rgba(245,158,11,.15), rgba(251,191,36,.08));
            border: 1px solid rgba(245,158,11,.35);
            border-radius: 12px;
            padding: 1.2rem 1.5rem;
            text-align: center;
        }
        .inr-value {
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--amber-l);
        }
        .inr-label {
            font-size: .75rem;
            color: var(--slate-400);
            text-transform: uppercase;
            letter-spacing: .08em;
            margin-top: .2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
