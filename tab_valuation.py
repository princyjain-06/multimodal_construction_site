"""
Tab 3 — Planning & Real Estate Valuation (Epic 3)
Budget calculator, INR valuation, materials estimation, and Pollinations AI 3D renders.
"""

from __future__ import annotations
import math
import urllib.parse
import streamlit as st
import plotly.graph_objects as go


# ── Constants ──────────────────────────────────────────────────────────────────

# Cost per sqft in INR by structure type
COST_PER_SQFT: dict[str, dict] = {
    "Residential (Low-Rise, ≤4F)":   {"tier1": 2800, "tier2": 2200, "tier3": 1700},
    "Residential (Mid-Rise, 5–15F)":  {"tier1": 3400, "tier2": 2700, "tier3": 2100},
    "Residential (High-Rise, >15F)":  {"tier1": 4200, "tier2": 3400, "tier3": 2600},
    "Commercial Office":              {"tier1": 4500, "tier2": 3600, "tier3": 2800},
    "Industrial / Warehouse":         {"tier1": 1800, "tier2": 1500, "tier3": 1200},
    "Mixed-Use Township":             {"tier1": 3800, "tier2": 3000, "tier3": 2300},
    "Infrastructure / Bridge":        {"tier1": 6000, "tier2": 5000, "tier3": 4000},
}

# Market appreciation multipliers at completion (structure type agnostic)
MARKET_MULT: dict[str, float] = {
    "Tier 1 (Mumbai, Delhi, Bengaluru, Chennai)": 1.35,
    "Tier 2 (Pune, Hyderabad, Ahmedabad, Kochi)": 1.22,
    "Tier 3 (Lucknow, Indore, Jaipur, Coimbatore)": 1.10,
}

# Steel (kg) and cement (bags of 50 kg) per sqft
MATERIAL_RATES: dict[str, dict] = {
    "Residential (Low-Rise, ≤4F)":   {"steel_kg": 4.5,  "cement_bags": 0.40},
    "Residential (Mid-Rise, 5–15F)":  {"steel_kg": 5.5,  "cement_bags": 0.48},
    "Residential (High-Rise, >15F)":  {"steel_kg": 7.0,  "cement_bags": 0.58},
    "Commercial Office":              {"steel_kg": 6.5,  "cement_bags": 0.55},
    "Industrial / Warehouse":         {"steel_kg": 3.5,  "cement_bags": 0.30},
    "Mixed-Use Township":             {"steel_kg": 6.0,  "cement_bags": 0.50},
    "Infrastructure / Bridge":        {"steel_kg": 12.0, "cement_bags": 0.80},
}

TIER_KEYS = {
    "Tier 1 (Mumbai, Delhi, Bengaluru, Chennai)": "tier1",
    "Tier 2 (Pune, Hyderabad, Ahmedabad, Kochi)": "tier2",
    "Tier 3 (Lucknow, Indore, Jaipur, Coimbatore)": "tier3",
}

MILESTONES = [
    ("Foundation & Substructure",  15),
    ("Structural Frame",           35),
    ("Masonry & Roofing",          55),
    ("MEP Rough-In",               70),
    ("Finishing & Interiors",      88),
    ("Handover Ready",            100),
]


# ── Calculation Engine ─────────────────────────────────────────────────────────

def _inr_format(amount_inr: float) -> str:
    """Format a large INR value into Lakhs or Crores."""
    if amount_inr >= 1e7:
        return f"₹ {amount_inr/1e7:.2f} Cr"
    return f"₹ {amount_inr/1e5:.2f} L"


def calculate_metrics(
    structure: str,
    sqft: float,
    location: str,
    completion_pct: float,
) -> dict:
    tier_key = TIER_KEYS[location]
    cost_sqft = COST_PER_SQFT[structure][tier_key]
    mat = MATERIAL_RATES[structure]
    market_mult = MARKET_MULT[location]

    total_budget = cost_sqft * sqft
    capex_incurred = total_budget * (completion_pct / 100)
    market_valuation = total_budget * market_mult * (0.6 + 0.4 * completion_pct / 100)

    steel_total_mt = (mat["steel_kg"] * sqft) / 1000
    cement_bags_total = mat["cement_bags"] * sqft
    steel_used = steel_total_mt * (completion_pct / 100)
    cement_used = cement_bags_total * (completion_pct / 100)

    return {
        "total_budget_inr": total_budget,
        "capex_incurred_inr": capex_incurred,
        "market_valuation_inr": market_valuation,
        "steel_total_mt": steel_total_mt,
        "steel_used_mt": steel_used,
        "cement_bags_total": cement_bags_total,
        "cement_bags_used": cement_used,
        "cost_per_sqft": cost_sqft,
        "market_mult": market_mult,
    }


def _current_milestone(pct: float) -> str:
    for name, threshold in MILESTONES:
        if pct <= threshold:
            return name
    return "Project Complete"


# ── Pollinations AI Render ─────────────────────────────────────────────────────

def _pollinations_url(prompt: str, width: int = 1024, height: int = 576, seed: int = 42) -> str:
    encoded = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&nologo=true&enhance=true"


def _build_render_prompt(structure: str, location: str, completion_pct: float) -> str:
    style_map = {
        "Residential (Low-Rise, ≤4F)":   "modern residential villa, lush green landscaping",
        "Residential (Mid-Rise, 5–15F)":  "contemporary mid-rise apartment complex with glass facade",
        "Residential (High-Rise, >15F)":  "sleek glass skyscraper luxury residential tower",
        "Commercial Office":              "futuristic glass commercial office tower with sky bridge",
        "Industrial / Warehouse":         "large modern industrial warehouse with steel structure",
        "Mixed-Use Township":             "smart township with mix of residential towers and commercial plazas",
        "Infrastructure / Bridge":        "iconic cable-stayed bridge over a river at golden hour",
    }
    style = style_map.get(structure, "modern construction")
    city_ref = location.split("(")[1].rstrip(")").split(",")[0].strip()
    stage = "under construction with cranes" if completion_pct < 80 else "nearly complete architectural"
    return (
        f"Photorealistic 3D architectural rendering of {style}, "
        f"inspired by {city_ref} skyline, {stage}, "
        f"dramatic sky, golden hour lighting, ultra-detailed, 8K, "
        f"architectural visualization style"
    )


# ── Charts ─────────────────────────────────────────────────────────────────────

def _budget_donut(capex: float, remaining: float) -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=["CapEx Incurred", "Remaining Budget"],
        values=[capex, remaining],
        hole=0.62,
        marker_colors=["#F59E0B", "#334155"],
        textinfo="percent",
        hovertemplate="%{label}: ₹%{value:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#94A3B8",
        showlegend=True,
        legend=dict(font=dict(color="#94A3B8", size=11)),
        margin=dict(t=20, b=20, l=20, r=20),
        height=220,
    )
    return fig


def _materials_bar(
    steel_total: float, steel_used: float,
    cement_total: float, cement_used: float,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Steel Used (MT)",
        x=["Steel (MT)"],
        y=[steel_used],
        marker_color="#F59E0B",
        width=0.35,
    ))
    fig.add_trace(go.Bar(
        name="Steel Remaining (MT)",
        x=["Steel (MT)"],
        y=[steel_total - steel_used],
        marker_color="#334155",
        width=0.35,
    ))
    fig.add_trace(go.Bar(
        name="Cement Used (Bags ÷ 10)",
        x=["Cement (Bags/10)"],
        y=[cement_used / 10],
        marker_color="#3B82F6",
        width=0.35,
    ))
    fig.add_trace(go.Bar(
        name="Cement Remaining (Bags ÷ 10)",
        x=["Cement (Bags/10)"],
        y=[(cement_total - cement_used) / 10],
        marker_color="#1E3A5F",
        width=0.35,
    ))
    fig.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#94A3B8",
        showlegend=True,
        legend=dict(font=dict(color="#94A3B8", size=10)),
        margin=dict(t=20, b=20, l=20, r=20),
        height=220,
        xaxis=dict(showgrid=False, color="#94A3B8"),
        yaxis=dict(showgrid=True, gridcolor="#334155", color="#94A3B8"),
    )
    return fig


# ── Main Render ────────────────────────────────────────────────────────────────

def render_valuation_tab(api_key: str, demo_mode: bool = False):  # api_key kept for interface uniformity
    st.markdown(
        """
        <div class="section-header">
            📐 Project Planning & Real Estate Valuation
        </div>
        <p style="color:#94A3B8;font-size:.88rem;margin-bottom:1rem;">
            Input project parameters to compute total budget, capital expenditure, current market valuation
            in INR, material requirements, and milestone progress. Conceptual 3D architectural renderings
            are generated via Pollinations AI.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # ── Input Form ─────────────────────────────────────────────────────────────
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            structure = st.selectbox(
                "🏢 Structure Type",
                list(COST_PER_SQFT.keys()),
                key="val_structure",
            )
            location = st.selectbox(
                "📍 Location Tier",
                list(TIER_KEYS.keys()),
                key="val_location",
            )
        with c2:
            sqft = st.number_input(
                "📏 Built-Up Area (sq ft)",
                min_value=500.0,
                max_value=5_000_000.0,
                value=5000.0,
                step=500.0,
                key="val_sqft",
            )
            completion_pct = st.slider(
                "⚙️ Project Completion %",
                min_value=0,
                max_value=100,
                value=45,
                step=1,
                key="val_completion",
            )

    calc_btn = st.button("📊 Calculate Metrics & Generate 3D Render", key="val_calc", use_container_width=False)

    if calc_btn or True:  # Always show live metrics on interaction
        m = calculate_metrics(structure, sqft, location, float(completion_pct))
        _render_valuation_results(m, structure, location, sqft, completion_pct)


def _render_valuation_results(m: dict, structure: str, location: str, sqft: float, completion_pct: float):
    st.markdown("<div class='glow-sep'></div>", unsafe_allow_html=True)

    # ── Key INR Metrics ────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div class="inr-display">
                <div class="inr-value">{_inr_format(m['total_budget_inr'])}</div>
                <div class="inr-label">Total Project Budget</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="inr-display">
                <div class="inr-value" style="color:#60A5FA;">{_inr_format(m['capex_incurred_inr'])}</div>
                <div class="inr-label">CapEx Incurred ({completion_pct}% complete)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="inr-display">
                <div class="inr-value" style="color:#34D399;">{_inr_format(m['market_valuation_inr'])}</div>
                <div class="inr-label">Current Market Asset Valuation</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Milestone Progress ─────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>🏁 Construction Milestones</div>", unsafe_allow_html=True)

    milestone_name = _current_milestone(completion_pct)
    st.markdown(
        f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem;">
            <span style="font-size:.85rem;color:#94A3B8;">Current Stage:</span>
            <span class="pill pill-amber">{milestone_name}</span>
        </div>
        <div class="progress-wrap" style="height:14px;margin-bottom:1rem;">
            <div class="progress-fill" style="width:{completion_pct}%;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Milestone step indicators
    mile_cols = st.columns(len(MILESTONES))
    for col, (name, threshold) in zip(mile_cols, MILESTONES):
        done = completion_pct >= threshold
        active = not done and completion_pct >= (threshold - 20)
        if done:
            color, icon = "#10B981", "✓"
        elif active:
            color, icon = "#F59E0B", "●"
        else:
            color, icon = "#334155", "○"
        col.markdown(
            f"""
            <div style="text-align:center;">
                <div style="font-size:1.2rem;color:{color};">{icon}</div>
                <div style="font-size:.6rem;color:{color};line-height:1.3;margin-top:2px;">{name}</div>
                <div style="font-size:.6rem;color:#475569;">{threshold}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='glow-sep'></div>", unsafe_allow_html=True)

    # ── Charts ─────────────────────────────────────────────────────────────────
    cc1, cc2, cc3 = st.columns([1, 1, 1])

    with cc1:
        st.markdown("<div style='text-align:center;font-size:.8rem;color:#94A3B8;margin-bottom:.3rem;'>Budget Utilization</div>", unsafe_allow_html=True)
        st.plotly_chart(
            _budget_donut(m["capex_incurred_inr"], m["total_budget_inr"] - m["capex_incurred_inr"]),
            use_container_width=True,
        )

    with cc2:
        st.markdown("<div style='text-align:center;font-size:.8rem;color:#94A3B8;margin-bottom:.3rem;'>Material Consumption</div>", unsafe_allow_html=True)
        st.plotly_chart(
            _materials_bar(
                m["steel_total_mt"], m["steel_used_mt"],
                m["cement_bags_total"], m["cement_bags_used"],
            ),
            use_container_width=True,
        )

    with cc3:
        st.markdown("<div style='text-align:center;font-size:.8rem;color:#94A3B8;margin-bottom:.3rem;'>Material Summary</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="card" style="margin-top:.5rem;">
                <div class="card-title">Steel Requirement</div>
                <div class="card-value">{m['steel_total_mt']:.1f} MT</div>
                <div class="card-sub">Used: {m['steel_used_mt']:.1f} MT · Remaining: {m['steel_total_mt']-m['steel_used_mt']:.1f} MT</div>
            </div>
            <div class="card">
                <div class="card-title">Cement Requirement</div>
                <div class="card-value">{m['cement_bags_total']:,.0f}</div>
                <div class="card-sub">Bags (50 kg) · Used: {m['cement_bags_used']:,.0f} bags</div>
            </div>
            <div class="card">
                <div class="card-title">Cost / sq ft</div>
                <div class="card-value">₹ {m['cost_per_sqft']:,}</div>
                <div class="card-sub">Market mult: {m['market_mult']}×</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── 3D Architectural Render ────────────────────────────────────────────────
    st.markdown("<div class='section-header'>🖼️ Conceptual 3D Architectural Render</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#94A3B8;font-size:.82rem;margin-bottom:.75rem;'>"
        "Rendered via Pollinations AI — photorealistic architectural visualization based on your project parameters.</p>",
        unsafe_allow_html=True,
    )

    render_prompt = _build_render_prompt(structure, location, float(completion_pct))
    render_url = _pollinations_url(render_prompt, seed=int(sqft) % 9999)

    col_r, col_info = st.columns([2, 1])
    with col_r:
        st.markdown(
            f"""
            <div class="render-box">
                <img src="{render_url}" alt="3D Architectural Render" 
                     style="width:100%;border-radius:12px;" 
                     onerror="this.style.display='none';this.nextElementSibling.style.display='block'"/>
                <div style="display:none;background:#1E293B;border-radius:12px;
                            padding:2rem;text-align:center;color:#94A3B8;">
                    🌐 Render unavailable (network). Check your connection.
                </div>
                <div class="render-overlay">
                    Pollinations AI · {structure} · {location.split('(')[0].strip()}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_info:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Render Prompt</div>
                <div style="font-size:.78rem;color:#94A3B8;font-style:italic;line-height:1.6;">
                    "{render_prompt[:200]}…"
                </div>
            </div>
            <div class="card">
                <div class="card-title">Project Summary</div>
                <div style="font-size:.8rem;color:#CBD5E1;line-height:1.8;">
                    📐 {sqft:,.0f} sq ft<br>
                    🏢 {structure.split('(')[0].strip()}<br>
                    📍 {location.split('(')[0].strip()}<br>
                    ⚙️ {completion_pct}% complete<br>
                    💰 {_inr_format(m['total_budget_inr'])} total
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
