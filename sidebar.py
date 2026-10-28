"""
Sidebar module: API key input, Demo Mode toggle, architecture overview, and feature navigation.
"""

import streamlit as st


def render_sidebar() -> tuple[str, bool]:
    """
    Render sidebar.
    Returns (api_key, demo_mode).
    demo_mode=True  → skip all API calls and show rich static results everywhere.
    """
    with st.sidebar:
        # ── Logo ──────────────────────────────────────────────────────────────
        st.markdown(
            """
            <div class="sidebar-logo">
                <div class="logo-icon">🏗️</div>
                <div class="logo-title">Construction AI</div>
                <div class="logo-sub">Skill Wallet · Capstone 1</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div class='glow-sep'></div>", unsafe_allow_html=True)

        api_key = ""
        demo_mode = True

        # ── Architecture Overview ─────────────────────────────────────────────
        st.markdown("### 🏛️ Architecture")
        st.markdown(
            """
            <div class="arch-box">
                <span>📦 Streamlit</span> — UI Framework<br>
                <span>🤖 Gemini 3.8 / 2.0 Flash</span> — Vision + Chat AI<br>
                <span>🖼️ Pollinations AI</span> — 3D Renders<br>
                <span>📊 Plotly</span> — Interactive Charts<br>
                <span>🐍 Python 3.10+</span> — Runtime<br>
                <span>☁️ Streamlit Cloud</span> — Deployment
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='glow-sep'></div>", unsafe_allow_html=True)

        # ── Feature Navigation ────────────────────────────────────────────────
        st.markdown("### 📋 Modules")
        features = [
            ("🦺", "Tab 1", "Site Safety & PPE Audit", "OSHA / IS 456 Compliance"),
            ("🔬", "Tab 2", "Crack Diagnostics", "Structural Integrity AI"),
            ("📐", "Tab 3", "Planning & Valuation", "INR Budget & 3D Renders"),
            ("🤖", "Tab 4", "Site Assistant", "Weather Advisory + Chatbot"),
        ]
        for icon, badge, name, desc in features:
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:.6rem;
                            background:#1E293B;border:1px solid #334155;
                            border-radius:10px;padding:.55rem .8rem;
                            margin-bottom:.4rem;">
                    <span style="font-size:1.2rem;">{icon}</span>
                    <div>
                        <div style="font-size:.78rem;font-weight:700;
                                    color:#F1F5F9;">{name}</div>
                        <div style="font-size:.68rem;color:#94A3B8;">{desc}</div>
                    </div>
                    <span style="margin-left:auto;font-size:.6rem;
                                 background:rgba(245,158,11,.2);color:#FCD34D;
                                 padding:2px 8px;border-radius:99px;
                                 font-weight:700;">{badge}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div class='glow-sep'></div>", unsafe_allow_html=True)

        # ── Standards ─────────────────────────────────────────────────────────
        st.markdown("### 📜 Standards")
        for std in ["OSHA 29 CFR 1926", "IS 456:2000", "IS 13920", "NBC 2016 India"]:
            st.markdown(
                f"<div style='font-size:.78rem;color:#94A3B8;padding:2px 0;'>"
                f"✓ <strong style='color:#FCD34D;'>{std}</strong></div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div style='text-align:center;font-size:.68rem;color:#475569;"
            "margin-top:1.5rem;'>v1.0.0 · 2026 · MIT License</div>",
            unsafe_allow_html=True,
        )

    return api_key, demo_mode
