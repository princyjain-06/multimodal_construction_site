"""
Tab 1 — Site Safety & PPE Audit (Epic 2)
Multimodal analysis of construction site photos for PPE compliance and hazard detection.
"""

from __future__ import annotations
import json
import streamlit as st
from PIL import Image

from ai_helper import (
    call_gemini_vision,
    extract_json_from_response,
    build_safety_prompt,
    DEMO_SAFETY_RESULT,
)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _score_color(score: int) -> str:
    if score >= 85:
        return "#10B981"
    if score >= 65:
        return "#F59E0B"
    if score >= 45:
        return "#F97316"
    return "#EF4444"


def _status_pill(status: str) -> str:
    mapping = {
        "Safe":           "pill-green",
        "Low Risk":       "pill-blue",
        "Moderate Risk":  "pill-amber",
        "High Risk":      "pill-orange",
        "Critical":       "pill-red",
    }
    cls = mapping.get(status, "pill-amber")
    return f"<span class='pill {cls}'>{status}</span>"


def _ppe_status_to_icon(status: str) -> tuple[str, str]:
    """Return (icon, css_class)."""
    if status == "Compliant":
        return "✅", "ppe-ok"
    if status == "Non-Compliant":
        return "❌", "ppe-ng"
    return "⚠️", "ppe-na"


def _hazard_css(severity: str) -> str:
    return {
        "Critical": "hazard-item critical",
        "High":     "hazard-item",
        "Medium":   "hazard-item medium",
        "Low":      "hazard-item low",
    }.get(severity, "hazard-item low")


def _severity_pill(severity: str) -> str:
    cls = {
        "Critical": "pill-red",
        "High":     "pill-orange",
        "Medium":   "pill-amber",
        "Low":      "pill-blue",
    }.get(severity, "pill-blue")
    return f"<span class='pill {cls}'>{severity}</span>"


# ── Main Render ────────────────────────────────────────────────────────────────

def render_safety_tab(api_key: str, demo_mode: bool = False):
    st.markdown(
        """
        <div class="section-header">
            🦺 Site Safety & PPE Compliance Audit
        </div>
        <p style="color:#94A3B8;font-size:.88rem;margin-bottom:1rem;">
            Upload a construction site photograph. The AI vision model will audit Personal Protective
            Equipment (PPE) compliance against <strong style="color:#FCD34D;">OSHA 29 CFR 1926</strong>
            and <strong style="color:#FCD34D;">IS 456:2000</strong> standards, detect hazards, and
            generate a downloadable safety report.
        </p>
        """,
        unsafe_allow_html=True,
    )

    col_upload, col_preview = st.columns([1.2, 1])

    with col_upload:
        uploaded = st.file_uploader(
            "📸 Upload Site Photo",
            type=["jpg", "jpeg", "png", "webp"],
            help="JPG / PNG / WEBP — max 50 MB",
            key="safety_uploader",
        )

    image: Image.Image | None = None
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        with col_preview:
            st.image(image, caption="Uploaded Site Photo", use_container_width=True)

    st.markdown("<div class='glow-sep'></div>", unsafe_allow_html=True)

    run_btn = st.button("🔍 Run PPE & Hazard Analysis", key="safety_run", use_container_width=False)

    if run_btn:
        result: dict | None = None

        if demo_mode or not api_key:
            # Demo / presentation mode — instant rich results
            result = DEMO_SAFETY_RESULT
        elif image is None:
            st.warning("⚠️ Please upload a construction site photo before running analysis.")
            return
        else:
            with st.spinner("🤖 Gemini Vision analysing site photo…"):
                raw = call_gemini_vision(api_key, build_safety_prompt(), image)
                if raw.startswith("__ERROR__"):
                    result = DEMO_SAFETY_RESULT
                else:
                    result = extract_json_from_response(raw) or DEMO_SAFETY_RESULT

        _render_safety_results(result, api_key)


def _render_safety_results(r: dict, api_key: str):
    """Render the full safety analysis dashboard."""
    score = r.get("safety_score", 0)
    status = r.get("overall_status", "Unknown")
    color = _score_color(score)

    # ── Row 1: Score + Status ──────────────────────────────────────────────────
    st.markdown("<div class='glow-sep'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="card" style="text-align:center;">
                <div class="card-title">Safety Score</div>
                <div class="card-value" style="color:{color};">{score}<span style="font-size:1.2rem;">/100</span></div>
                <div class="card-sub">AI-computed PPE & Hazard Index</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="card" style="text-align:center;">
                <div class="card-title">Overall Status</div>
                <div style="margin-top:.5rem;">{_status_pill(status)}</div>
                <div class="card-sub" style="margin-top:.5rem;">{r.get('standard','—')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    hazards = r.get("site_hazards", [])
    critical_count = sum(1 for h in hazards if h.get("severity") == "Critical")
    high_count = sum(1 for h in hazards if h.get("severity") == "High")

    with c3:
        st.markdown(
            f"""
            <div class="card" style="text-align:center;">
                <div class="card-title">Critical Hazards</div>
                <div class="card-value" style="color:#EF4444;">{critical_count}</div>
                <div class="card-sub">Require immediate action</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div class="card" style="text-align:center;">
                <div class="card-title">High Hazards</div>
                <div class="card-value" style="color:#F97316;">{high_count}</div>
                <div class="card-sub">Require same-shift resolution</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Score progress bar ─────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="margin:.5rem 0 1.5rem;">
            <div style="display:flex;justify-content:space-between;
                        font-size:.75rem;color:#94A3B8;margin-bottom:4px;">
                <span>Safety Score</span><span>{score}/100</span>
            </div>
            <div class="progress-wrap">
                <div class="progress-fill" style="width:{score}%;
                     background:linear-gradient(90deg,{color},{color}cc);"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── PPE Detection ──────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>🧢 PPE Detection Checklist</div>", unsafe_allow_html=True)

    ppe = r.get("ppe_detection", {})
    ppe_labels = {
        "helmets":          "Hard Hats / Helmets",
        "high_vis_vests":   "High-Visibility Vests",
        "steel_toe_boots":  "Steel-Toe Boots",
        "safety_harnesses": "Safety Harnesses (Fall Arrest)",
        "safety_glasses":   "Safety Glasses / Face Shields",
    }

    ppe_col1, ppe_col2 = st.columns(2)
    items = list(ppe.items())
    for idx, (key, val) in enumerate(items):
        label = ppe_labels.get(key, key.replace("_", " ").title())
        icon, css = _ppe_status_to_icon(val.get("status", "Partial"))
        wearing = val.get("workers_wearing", "—")
        total = val.get("total_workers", "—")
        col = ppe_col1 if idx % 2 == 0 else ppe_col2
        with col:
            st.markdown(
                f"""
                <div class="ppe-item {css}">
                    <span style="font-size:1.1rem;">{icon}</span>
                    <div style="flex:1;">
                        <div style="font-weight:600;">{label}</div>
                        <div style="font-size:.75rem;color:#94A3B8;">
                            {wearing}/{total} workers · {val.get('status','—')}
                        </div>
                    </div>
                    {_severity_pill(val.get('status','Partial').replace('Compliant','Safe').replace('Non-Compliant','High'))}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Site Hazards ───────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>⚠️ Identified Site Hazards & Remedies</div>", unsafe_allow_html=True)

    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    sorted_hazards = sorted(hazards, key=lambda h: severity_order.get(h.get("severity", "Low"), 4))

    for h in sorted_hazards:
        severity = h.get("severity", "Low")
        st.markdown(
            f"""
            <div class="{_hazard_css(severity)}">
                <div class="hazard-title">
                    {_severity_pill(severity)} &nbsp; {h.get('hazard','—')}
                </div>
                <div class="hazard-remedy">
                    <strong style="color:#FCD34D;">OSHA Ref:</strong> {h.get('osha_ref','—')} &nbsp;|&nbsp;
                    <strong style="color:#FCD34D;">Remedy:</strong> {h.get('remedy','—')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Download JSON Report ───────────────────────────────────────────────────
    st.markdown("<div class='glow-sep'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>📥 Download Report</div>", unsafe_allow_html=True)

    json_str = json.dumps(r, indent=2)
    st.download_button(
        label="⬇️ Download Safety Audit JSON Report",
        data=json_str,
        file_name="safety_audit_report.json",
        mime="application/json",
        key="safety_download",
    )

    with st.expander("🔍 View Raw JSON Report"):
        st.markdown(
            f"<div class='json-display'><pre>{json_str}</pre></div>",
            unsafe_allow_html=True,
        )
