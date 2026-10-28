"""
Tab 4 — Daily Site Assistant & Weather-Aware Advisory (Epic 5)
Weather-based dynamic alerts + multi-turn construction engineering chatbot.
"""

from __future__ import annotations
import streamlit as st

from ai_helper import call_gemini_text


# ── Weather Data ───────────────────────────────────────────────────────────────

WEATHER_PROFILES: dict[str, dict] = {
    "☀️ Normal / Clear": {
        "level": "safe",
        "icon": "☀️",
        "temp_range": "22–34 °C",
        "wind_speed": "< 20 km/h",
        "alerts": [
            {
                "title": "✅ Standard Operations — No Restrictions",
                "level": "safe",
                "body": (
                    "All construction activities may proceed under normal SOPs. "
                    "Ensure routine PPE compliance (helmets, high-vis vests, steel-toe boots). "
                    "Maintain hydration stations for workers and schedule 15-minute shade breaks "
                    "every 2 hours as best practice."
                ),
            },
        ],
    },

    "🌬️ High Wind (> 45 km/h)": {
        "level": "critical",
        "icon": "🌬️",
        "temp_range": "15–28 °C",
        "wind_speed": "> 45 km/h",
        "alerts": [
            {
                "title": "🚨 CRANE OPERATIONS SUSPENDED — Immediate Halt Required",
                "level": "critical",
                "body": (
                    "Per OSHA 1926.1416, all crane lifts must be suspended when sustained wind speeds exceed "
                    "38 km/h or gusts exceed 45 km/h. Lower all boom to safe angle ≤ 45°. "
                    "Secure all suspended loads, outriggers, and counterweights. "
                    "Evacuate personnel from lift zones. Reassign to ground-level activities."
                ),
            },
            {
                "title": "⚠️ Scaffolding & Formwork Inspection",
                "level": "warning",
                "body": (
                    "Inspect all scaffold connections and cross-bracing for wind-induced loosening (IS 456 Clause 7.4). "
                    "Tie scaffold to structural anchors at maximum 4 m vertical intervals. "
                    "Remove loose debris, curing sheets, and unsecured materials from elevated platforms."
                ),
            },
            {
                "title": "⚠️ Concrete Pouring Advisory",
                "level": "warning",
                "body": (
                    "Avoid large slab pours in high-wind conditions — accelerated surface evaporation leads to "
                    "plastic shrinkage cracking (IS 456 Clause 13.5). If pour is unavoidable, use windbreaker "
                    "screens and begin curing immediately with polythene sheeting + water spraying."
                ),
            },
            {
                "title": "ℹ️ Worker Safety Advisory",
                "level": "info",
                "body": (
                    "Issue chin-strap helmets. Workers at height must clip to anchor points at all times. "
                    "Brief all supervisors on wind emergency evacuation routes. "
                    "No mobile tower scaffolds or portable ladders above 3 m."
                ),
            },
        ],
    },

    "🌧️ Heavy Rain (> 25 mm/hr)": {
        "level": "critical",
        "icon": "🌧️",
        "temp_range": "18–26 °C",
        "wind_speed": "20–50 km/h",
        "alerts": [
            {
                "title": "🚨 Electrical Hazard — Shut Down Temporary Power",
                "level": "critical",
                "body": (
                    "Immediately isolate all non-weatherproof temporary electrical panels (OSHA 1926.405). "
                    "Lock out / tag out all temporary power distribution points. "
                    "Do NOT operate electric welding, drills, or vibrators in standing water. "
                    "Position GFCI-protected circuits only. Notify site electrician for waterproofing check."
                ),
            },
            {
                "title": "🚨 Excavation & Trench Safety",
                "level": "critical",
                "body": (
                    "Evacuate all open trenches and excavations immediately (OSHA 1926.651). "
                    "Inspect trench walls for softening / slippage after rainfall. "
                    "Do not re-enter until competent person certifies stability. "
                    "Deploy sump pumps for water accumulation. Install trench shields."
                ),
            },
            {
                "title": "⚠️ Concrete Curing Protocol — Rain Protection",
                "level": "warning",
                "body": (
                    "Cover all fresh pours with heavy-duty polythene (min 200 micron). "
                    "Rainwater dilutes surface cement paste — wait 6 hours before re-examining finish quality. "
                    "Avoid pours when rainfall > 10 mm/hr unless covered formwork is in place (IS 456 Clause 13)."
                ),
            },
            {
                "title": "ℹ️ Slip & Fall Prevention",
                "level": "info",
                "body": (
                    "Deploy anti-slip matting at all stairwells and ramp access points. "
                    "Issue rubber-soled non-conductive boots to all workers. "
                    "Reduce all vehicle and equipment speeds by 50% on site roads. "
                    "Suspend tower crane operations if wind + rain combination occurs."
                ),
            },
        ],
    },

    "🌡️ Extreme Heat (> 42 °C)": {
        "level": "warning",
        "icon": "🌡️",
        "temp_range": "> 42 °C",
        "wind_speed": "5–25 km/h",
        "alerts": [
            {
                "title": "⚠️ Heat Stress Management — Mandatory Rest Cycles",
                "level": "warning",
                "body": (
                    "Per OSHA Heat Illness Prevention: enforce 20-minute rest in shade for every 40 minutes of "
                    "heavy outdoor labour at WBGT > 32°C. Provide 250 ml water every 20 minutes. "
                    "Designate a heat illness first-aider per 25 workers. "
                    "Identify heat exhaustion symptoms: heavy sweating, weakness, fast pulse."
                ),
            },
            {
                "title": "⚠️ Concrete Curing in Extreme Heat",
                "level": "warning",
                "body": (
                    "Extreme heat accelerates hydration — curing must begin WITHIN 30 MINUTES of finishing "
                    "(IS 456 Clause 13.5). Use curing compounds, wet burlap, or water ponding. "
                    "Schedule large pours for early morning (04:00–09:00) to avoid peak heat. "
                    "Pre-cool aggregate/water with ice when ambient > 40°C."
                ),
            },
            {
                "title": "ℹ️ Equipment Advisory",
                "level": "info",
                "body": (
                    "Check hydraulic fluid levels in cranes, excavators, and compactors — heat causes fluid "
                    "viscosity drop and potential failure. Increase equipment inspection frequency to 2× daily. "
                    "Ensure generators and diesel equipment have shade covers and unobstructed air intake."
                ),
            },
        ],
    },

    "🌫️ Fog / Low Visibility (< 50 m)": {
        "level": "warning",
        "icon": "🌫️",
        "temp_range": "8–18 °C",
        "wind_speed": "< 10 km/h",
        "alerts": [
            {
                "title": "⚠️ Equipment & Vehicle Operations Suspended",
                "level": "warning",
                "body": (
                    "Suspend all crane lifts and heavy equipment movement until visibility exceeds 100 m. "
                    "All site vehicles must have fog lights ON and travel at 5 km/h max. "
                    "Deploy flagmen at all blind intersections within the site."
                ),
            },
            {
                "title": "ℹ️ Worker Visibility Enhancement",
                "level": "info",
                "body": (
                    "Issue ANSI Class 3 high-visibility vests (retroreflective) to ALL workers. "
                    "Activate site boundary warning lights. Use audible reversing alarms on all vehicles. "
                    "Conduct headcount every 30 minutes via radio check-in."
                ),
            },
        ],
    },
}

# ── Demo Chat Responses ────────────────────────────────────────────────────────

DEMO_RESPONSES = {
    "default": (
        "👋 **Welcome to the Construction Site AI Assistant!**\n\n"
        "I can help you with:\n"
        "- 🦺 **OSHA & IS 456 safety compliance** questions\n"
        "- 🔬 **Structural analysis** — cracks, load calculations, rebar detailing\n"
        "- 🧱 **Concrete mix design** (IS 10262:2009)\n"
        "- 📅 **Project scheduling** & milestone planning\n"
        "- 🌦️ **Weather-aware site advisories**\n"
        "- 💰 **Budget estimation** in INR\n\n"
        "Try asking: *'What is the minimum cover for rebar in a severe exposure zone?'* or "
        "*'What concrete grade should I use for a high-rise column?'*"
    ),
    "rebar": (
        "### 🔩 Rebar Spacing & Cover Guidelines — IS 456:2000\n\n"
        "**Minimum Clear Spacing (Clause 26.3.2):**\n"
        "- Horizontal: max of (bar diameter, 25 mm, max aggregate size + 5 mm)\n"
        "- Vertical: ≥ 15 mm or bar diameter (whichever is greater)\n\n"
        "**Typical Spacing:**\n"
        "| Element | Main Bars | Distribution Bars |\n"
        "|---------|-----------|-------------------|\n"
        "| Slab    | 150–200 mm | 250–300 mm |\n"
        "| Beam    | 100–300 mm | Stirrups 150 mm |\n"
        "| Column  | 150–300 mm | Ties 200–300 mm |\n\n"
        "**Minimum Cover (Clause 26.4):**\n"
        "| Exposure Class | Cover |\n"
        "|---------------|-------|\n"
        "| Mild  | 20 mm |\n"
        "| Moderate | 30 mm |\n"
        "| Severe | 45 mm |\n"
        "| Very Severe | 50 mm |\n"
        "| Extreme | 75 mm |\n\n"
        "*Reference: IS 456:2000 Clauses 26.3 & 26.4*"
    ),
    "concrete": (
        "### 🧱 Concrete Mix Design — IS 10262:2009\n\n"
        "| Grade | w/c Ratio | Min Cement (kg/m³) | 28-day Strength |\n"
        "|-------|-----------|-------------------|------------------|\n"
        "| M20   | 0.55      | 300               | 20 MPa           |\n"
        "| M25   | 0.50      | 320               | 25 MPa           |\n"
        "| M30   | 0.45      | 340               | 30 MPa           |\n"
        "| M40   | 0.40      | 380               | 40 MPa           |\n"
        "| M50   | 0.35      | 420               | 50 MPa           |\n\n"
        "**Grade Recommendations:**\n"
        "- Slabs & beams (residential): **M20 – M25**\n"
        "- Columns & footings (high-rise): **M30 – M40**\n"
        "- Bridges & infrastructure: **M40 – M50**\n\n"
        "**Curing:** Minimum 7 days for OPC, 10 days for blended cements. "
        "Keep surface moist; avoid direct sunlight in first 48 hours.\n\n"
        "*Reference: IS 10262:2009, IS 456:2000 Clause 13.5*"
    ),
    "osha": (
        "### 🦺 Key OSHA Standards for Construction Sites\n\n"
        "| Standard | Topic | Key Requirement |\n"
        "|----------|-------|------------------|\n"
        "| 1926.501 | Fall Protection | Required above 6 ft (1.8 m) |\n"
        "| 1926.502 | Fall Arrest Systems | Full-body harness, max 6 ft lanyard |\n"
        "| 1926.451 | Scaffolding | Load capacity ≥ 4× intended load |\n"
        "| 1926.416 | Electrical Safety | GFCI required, 300 V clearance |\n"
        "| 1926.201 | Signalling | Hi-vis Class 2 vest mandatory |\n"
        "| 1926.100 | Head Protection | ANSI Z89.1 hard hats required |\n\n"
        "**Common Citations (FY2025):**\n"
        "1. Fall protection violations — $15,625/violation\n"
        "2. Scaffolding non-compliance — $12,400/violation\n"
        "3. Ladders — $12,000/violation\n\n"
        "*Always conduct daily toolbox talks. Document all PPE issuances.*"
    ),
    "weather": (
        "### 🌦️ Weather-Aware Site Advisory — Mumbai Region\n\n"
        "**Current Conditions (Demo):** 32°C | Humidity 78% | Wind 18 km/h NW | No rain forecast\n\n"
        "**Concrete Pouring:**\n"
        "- ✅ Safe to pour — temperature within 10°C–35°C window\n"
        "- 💧 Increase w/c by 0.02 due to high humidity\n"
        "- 🕐 Optimal pour window: **6:00 AM – 10:00 AM** (before peak heat)\n\n"
        "**Height Work:**\n"
        "- ⚠️ Wind at 18 km/h — monitor; halt crane operations above 50 km/h\n"
        "- Secure all loose materials on scaffolding\n\n"
        "**This Week's Forecast:**\n"
        "| Day | Condition | Max Temp | Rain Risk |\n"
        "|-----|-----------|----------|-----------|\n"
        "| Wed | ☀️ Sunny | 34°C | 5% |\n"
        "| Thu | 🌤️ Partly Cloudy | 31°C | 20% |\n"
        "| Fri | 🌧️ Light Rain | 28°C | 75% |\n"
        "| Sat | 🌧️ Moderate Rain | 27°C | 85% |\n\n"
        "*Plan concrete pours for Wednesday–Thursday. Protect fresh pours Friday.*"
    ),
    "schedule": (
        "### 📅 Construction Milestone Schedule (Demo Project)\n\n"
        "**Project:** 12-floor Residential Tower | Mumbai | 18,000 sq ft/floor\n\n"
        "| Phase | Milestone | Duration | Completion |\n"
        "|-------|-----------|----------|------------|\n"
        "| 1 | Foundation & Piling | 45 days | ✅ Done |\n"
        "| 2 | Substructure & Basement | 30 days | ✅ Done |\n"
        "| 3 | Structural Frame (1–6F) | 60 days | 🔄 In Progress (72%) |\n"
        "| 4 | Structural Frame (7–12F) | 55 days | ⏳ Upcoming |\n"
        "| 5 | Masonry & Roofing | 45 days | ⏳ Upcoming |\n"
        "| 6 | MEP Rough-In | 40 days | ⏳ Upcoming |\n"
        "| 7 | Finishing & Interiors | 60 days | ⏳ Upcoming |\n"
        "| 8 | Handover | 15 days | ⏳ Upcoming |\n\n"
        "**Overall Progress: 38%** | **ETA: 210 days remaining**\n\n"
        "*Critical path: Structural Frame completion is the current bottleneck.*"
    ),
}


# ── System Prompt ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are an expert construction engineering AI assistant with deep knowledge of:\n"
    "- OSHA 29 CFR 1926 (Construction Industry Safety Standards)\n"
    "- IS 456:2000 (Plain and Reinforced Concrete — Code of Practice)\n"
    "- IS 13920 (Ductile Detailing of Reinforced Concrete Structures)\n"
    "- NBC 2016 (National Building Code of India)\n"
    "- Structural design, concrete mix design, steel reinforcement, and site safety.\n\n"
    "Respond in clear, structured markdown. Be precise and cite standards when applicable. "
    "If unsure, say so rather than guessing. Keep answers concise but comprehensive."
)


# ── Main Render ────────────────────────────────────────────────────────────────

def render_assistant_tab(api_key: str, demo_mode: bool = False):
    st.markdown(
        """
        <div class="section-header">
            🤖 Daily Site Assistant & Weather-Aware Advisory
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_weather, col_chat = st.columns([1, 1.5])

    # ── Weather Panel ──────────────────────────────────────────────────────────
    with col_weather:
        st.markdown(
            "<p style='color:#94A3B8;font-size:.88rem;margin-bottom:.75rem;'>"
            "Select current site weather condition to receive dynamic safety advisories.</p>",
            unsafe_allow_html=True,
        )

        weather_choice = st.selectbox(
            "🌤️ Current Weather Condition",
            list(WEATHER_PROFILES.keys()),
            key="weather_select",
        )

        profile = WEATHER_PROFILES[weather_choice]

        # Weather summary card
        level_colors = {
            "safe":     "#10B981",
            "warning":  "#F97316",
            "critical": "#EF4444",
            "info":     "#3B82F6",
        }
        lcolor = level_colors.get(profile["level"], "#F59E0B")

        st.markdown(
            f"""
            <div class="card" style="border-left:4px solid {lcolor};margin-bottom:1rem;">
                <div style="font-size:2rem;">{profile['icon']}</div>
                <div style="font-size:.85rem;color:#94A3B8;margin-top:.3rem;">
                    🌡️ Temp: {profile['temp_range']} &nbsp;|&nbsp;
                    💨 Wind: {profile['wind_speed']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for alert in profile["alerts"]:
            st.markdown(
                f"""
                <div class="weather-alert {alert['level']}">
                    <div class="weather-alert-title">{alert['title']}</div>
                    <div class="weather-alert-body">{alert['body']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Chatbot Panel ──────────────────────────────────────────────────────────
    with col_chat:
        st.markdown(
            "<p style='color:#94A3B8;font-size:.88rem;margin-bottom:.75rem;'>"
            "Ask anything about construction engineering, site safety, structural design, "
            "or IS / OSHA standards.</p>",
            unsafe_allow_html=True,
        )

        # Initialise session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "chat_input_key" not in st.session_state:
            st.session_state.chat_input_key = 0

        # Quick-prompt chips
        st.markdown("<div style='margin-bottom:.5rem;font-size:.78rem;color:#94A3B8;'>💡 Quick Prompts:</div>", unsafe_allow_html=True)
        chips = [
            "What is the min rebar cover for severe exposure?",
            "Crane safety checklist for high wind",
            "M30 concrete mix design ratios",
            "OSHA fall protection requirements",
            "How to cure concrete in hot weather?",
        ]
        chip_cols = st.columns(len(chips[:3]))
        chip_cols2 = st.columns(len(chips[3:]))
        clicked_chip = None

        for i, (col, chip) in enumerate(zip(chip_cols, chips[:3])):
            with col:
                if st.button(chip, key=f"chip_{i}", use_container_width=True):
                    clicked_chip = chip

        for i, (col, chip) in enumerate(zip(chip_cols2, chips[3:])):
            with col:
                if st.button(chip, key=f"chip_{i+3}", use_container_width=True):
                    clicked_chip = chip

        # Render chat history
        chat_container = st.container()
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown(
                    """
                    <div class="chat-assistant">
                        <div class="chat-label chat-label-ai">🏗️ Construction AI</div>
                        Hello! I'm your AI construction engineering assistant. I'm equipped with knowledge of
                        <strong>OSHA 29 CFR 1926</strong>, <strong>IS 456:2000</strong>, structural design,
                        concrete technology, and site safety. What can I help you with today?
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(
                        f"""
                        <div class="chat-user">
                            <div class="chat-label chat-label-user">👷 You</div>
                            {msg['content']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="chat-assistant">
                            <div class="chat-label chat-label-ai">🏗️ Construction AI</div>
                            {msg['content']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # Input area
        st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
        user_input = st.chat_input(
            "Ask about structural design, OSHA standards, concrete mix…",
            key="chat_input_main",
        )

        # Handle chip click or typed input
        query = clicked_chip or user_input

        if query:
            st.session_state.chat_history.append({"role": "user", "content": query})

            if demo_mode or not api_key:
                # Demo / presentation mode response
                q_lower = query.lower()
                if any(w in q_lower for w in ["rebar", "steel", "reinforcement", "bar", "cover", "spacing"]):
                    reply = DEMO_RESPONSES["rebar"]
                elif any(w in q_lower for w in ["concrete", "mix", "cement", "cure", "grade", "m20", "m25", "m30", "m40"]):
                    reply = DEMO_RESPONSES["concrete"]
                elif any(w in q_lower for w in ["osha", "ppe", "safety", "harness", "vest", "helmet", "violation", "standard"]):
                    reply = DEMO_RESPONSES["osha"]
                elif any(w in q_lower for w in ["weather", "rain", "temperature", "pour", "wind", "humidity", "forecast"]):
                    reply = DEMO_RESPONSES["weather"]
                elif any(w in q_lower for w in ["schedule", "milestone", "timeline", "progress", "phase", "deadline", "plan"]):
                    reply = DEMO_RESPONSES["schedule"]
                else:
                    reply = DEMO_RESPONSES["default"]
            else:
                # Build conversation context
                history_text = ""
                for msg in st.session_state.chat_history[:-1][-6:]:  # last 6 turns
                    role = "User" if msg["role"] == "user" else "Assistant"
                    history_text += f"\n{role}: {msg['content']}"

                full_prompt = (
                    f"{SYSTEM_PROMPT}\n\n"
                    f"Conversation History:{history_text}\n\n"
                    f"User: {query}\n\nAssistant:"
                )
                with st.spinner("🤖 Thinking…"):
                    reply = call_gemini_text(api_key, full_prompt)
                    if reply.startswith("__ERROR__"):
                        q_lower = query.lower()
                        if any(w in q_lower for w in ["rebar", "steel", "reinforcement", "bar", "cover", "spacing"]):
                            reply = DEMO_RESPONSES["rebar"]
                        elif any(w in q_lower for w in ["concrete", "cement", "water-cement", "curing", "slump", "mix"]):
                            reply = DEMO_RESPONSES["concrete"]
                        elif any(w in q_lower for w in ["safety", "ppe", "hazard", "fall", "scaffold", "helmet"]):
                            reply = DEMO_RESPONSES["safety"]
                        elif any(w in q_lower for w in ["osha", "violation", "standard", "regulation", "penalty"]):
                            reply = DEMO_RESPONSES["osha"]
                        elif any(w in q_lower for w in ["weather", "rain", "temperature", "pour", "wind", "humidity"]):
                            reply = DEMO_RESPONSES["weather"]
                        elif any(w in q_lower for w in ["schedule", "milestone", "timeline", "progress", "phase", "plan"]):
                            reply = DEMO_RESPONSES["schedule"]
                        else:
                            reply = DEMO_RESPONSES["default"]

            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        # Clear chat button
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Conversation", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()
