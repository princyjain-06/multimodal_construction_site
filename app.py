"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1
"""

import streamlit as st
from styles import inject_css
from sidebar import render_sidebar
from tab_safety import render_safety_tab
from tab_crack import render_crack_tab
from tab_valuation import render_valuation_tab
from tab_assistant import render_assistant_tab

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Inject Custom CSS ─────────────────────────────────────────────────────────
inject_css()

# ─── Sidebar ───────────────────────────────────────────────────────────────────
api_key, demo_mode = render_sidebar()

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="main-header">
        <div class="header-badge">⚡ AI-POWERED</div>
        <h1 class="header-title">🏗️ Multimodal Construction Intelligence Platform</h1>
        <p class="header-subtitle">
            Skill Wallet Capstone Project 1 &nbsp;|&nbsp;
            Powered by Google Gemini &nbsp;|&nbsp;
            OSHA &amp; IS 456 Compliant Analysis
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Banner ────────────────────────────────────────────────────────────────────
if demo_mode:
    st.markdown(
        """
        <div class="demo-banner" style="background:linear-gradient(90deg,#7C3AED22,#F59E0B22);
             border:1px solid #F59E0B55;">
            🎬 <strong>Demo / Presentation Mode Active</strong> —
            All tabs show rich realistic results instantly. Toggle off in the sidebar to use a live API key.
        </div>
        """,
        unsafe_allow_html=True,
    )
elif not api_key:
    st.markdown(
        """
        <div class="demo-banner">
            🔮 <strong>Demonstration Mode Active</strong> —
            Enter your Google Gemini API key in the sidebar to unlock live AI analysis.
            All features remain accessible with realistic sample outputs.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─── Navigation Tabs ───────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Site Safety & PPE Audit",
    "🔬 Crack Diagnostics",
    "📐 Planning & Valuation",
    "🤖 Site Assistant",
])

with tab1:
    render_safety_tab(api_key, demo_mode=demo_mode)

with tab2:
    render_crack_tab(api_key, demo_mode=demo_mode)

with tab3:
    render_valuation_tab(api_key, demo_mode=demo_mode)

with tab4:
    render_assistant_tab(api_key, demo_mode=demo_mode)
