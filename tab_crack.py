"""
Tab 2 — Crack Diagnostics & Structural Integrity (Epic 2)
Multimodal defect classification for concrete/wall surfaces.
"""

from __future__ import annotations
import json
import streamlit as st
from PIL import Image

from ai_helper import (
    call_gemini_vision,
    extract_json_from_response,
    build_crack_prompt,
    DEMO_CRACK_RESULT,
)


# ── Helpers ────────────────────────────────────────────────────────────────────

URGENCY_COLORS = {
    "Low":      "#10B981",
    "Medium":   "#F59E0B",
    "High":     "#F97316",
    "Critical": "#EF4444",
}

DEFECT_ICONS = {
    "Hairline":           "🔍",
    "Settlement":         "⬇️",
    "Structural Shear":   "⚡",
    "Thermal Expansion":  "🌡️",
    "Spalling":           "💥",
    "Other":              "🔎",
}

RISK_COLORS = {
    "Low":           "#10B981",
    "Moderate":      "#F59E0B",
    "Moderate-High": "#F97316",
    "High":          "#EF4444",
    "Critical":      "#DC2626",
}


def _urgency_label(u: str) -> str:
    key = u.split("–")[0].strip() if "–" in u else u.split("-")[0].strip()
    key = key.split("—")[0].strip()
    color = URGENCY_COLORS.get(key, "#F59E0B")
    return f"<span class='pill' style='background:rgba(255,255,255,.08);color:{color};border:1px solid {color}55;'>{u}</span>"


def _risk_badge(risk: str) -> str:
    color = RISK_COLORS.get(risk, "#F59E0B")
    return f"<span class='pill' style='background:{color}22;color:{color};border:1px solid {color}55;'>{risk}</span>"


# ── Main Render ────────────────────────────────────────────────────────────────

def render_crack_tab(api_key: str, demo_mode: bool = False):
    st.markdown(
        """
        <div class="section-header">
            🔬 Crack Diagnostics & Structural Integrity Analysis
        </div>
        <p style="color:#94A3B8;font-size:.88rem;margin-bottom:1rem;">
            Upload a photograph of a concrete surface, wall, beam, or slab.
            The AI will classify the defect type, estimate crack dimensions, identify root causes,
            and prescribe engineering repair methods per <strong style="color:#FCD34D;">IS 456:2000</strong>.
        </p>
        """,
        unsafe_allow_html=True,
    )

    col_up, col_pv = st.columns([1.2, 1])

    with col_up:
        uploaded = st.file_uploader(
            "📸 Upload Concrete / Wall Surface Photo",
            type=["jpg", "jpeg", "png", "webp"],
            key="crack_uploader",
        )

    image: Image.Image | None = None
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        with col_pv:
            st.image(image, caption="Uploaded Surface Photo", use_container_width=True)

    st.markdown("<div class='glow-sep'></div>", unsafe_allow_html=True)

    run_btn = st.button("🔬 Diagnose Cracks & Defects", key="crack_run")

    if run_btn:
        result: dict | None = None

        if demo_mode or not api_key:
            result = DEMO_CRACK_RESULT
        elif image is None:
            st.warning("⚠️ Please upload a concrete/wall surface photo before running diagnosis.")
            return
        else:
            with st.spinner("🤖 Gemini Vision diagnosing crack patterns…"):
                raw = call_gemini_vision(api_key, build_crack_prompt(), image)
                if raw.startswith("__ERROR__"):
                    result = DEMO_CRACK_RESULT
                else:
                    result = extract_json_from_response(raw) or DEMO_CRACK_RESULT

        _render_crack_results(result)


def _render_crack_results(r: dict):
    """Render crack diagnostics dashboard."""
    defect_type = r.get("defect_type", "Unknown")
    icon = DEFECT_ICONS.get(defect_type.split()[0] if defect_type else "Other", "🔎")

    st.markdown("<div class='glow-sep'></div>", unsafe_allow_html=True)

    # ── Primary defect card ────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="defect-card">
            <div style="display:flex;align-items:center;gap:.75rem;margin-bottom:.5rem;">
                <span style="font-size:2rem;">{icon}</span>
                <div>
                    <div class="defect-type">{defect_type}</div>
                    <div style="font-size:.78rem;color:#94A3B8;">IS Standard Ref: {r.get('is_standard_ref','—')}</div>
                </div>
                <div style="margin-left:auto;">
                    {_risk_badge(r.get('structural_risk','Unknown'))}
                </div>
            </div>
            <div class="defect-meta">
                <div class="defect-meta-item">
                    <div class="defect-meta-label">Crack Width</div>
                    <div class="defect-meta-value">{r.get('crack_width_mm','—')} mm</div>
                </div>
                <div class="defect-meta-item">
                    <div class="defect-meta-label">Crack Length</div>
                    <div class="defect-meta-value">{r.get('crack_length_mm','—')} mm</div>
                </div>
                <div class="defect-meta-item">
                    <div class="defect-meta-label">Orientation</div>
                    <div class="defect-meta-value">{r.get('orientation','—')}</div>
                </div>
                <div class="defect-meta-item">
                    <div class="defect-meta-label">Urgency</div>
                    <div style="margin-top:.15rem;">{_urgency_label(r.get('urgency','—'))}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Root Causes ────────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>🌱 Root Causes</div>", unsafe_allow_html=True)
    causes = r.get("root_causes", [])
    for i, cause in enumerate(causes, 1):
        st.markdown(
            f"""
            <div style="display:flex;align-items:flex-start;gap:.6rem;
                        background:#1E293B;border:1px solid #334155;
                        border-radius:8px;padding:.6rem .9rem;margin-bottom:.35rem;">
                <span style="background:#F59E0B22;color:#FCD34D;
                             border-radius:50%;width:22px;height:22px;
                             display:flex;align-items:center;justify-content:center;
                             font-size:.75rem;font-weight:700;flex-shrink:0;">{i}</span>
                <span style="color:#CBD5E1;font-size:.87rem;">{cause}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Recommended Repairs ───────────────────────────────────────────────────
    st.markdown("<div class='section-header'>🔧 Recommended Engineering Repairs</div>", unsafe_allow_html=True)

    repairs = r.get("recommended_repairs", [])
    if repairs:
        repair_tabs = st.tabs([rep.get("method", f"Method {i+1}") for i, rep in enumerate(repairs)])
        for tab, rep in zip(repair_tabs, repairs):
            with tab:
                st.markdown(
                    f"""
                    <div class="card">
                        <div style="font-size:1rem;font-weight:700;color:#FCD34D;margin-bottom:.6rem;">
                            🔧 {rep.get('method','—')}
                        </div>
                        <p style="color:#CBD5E1;font-size:.87rem;line-height:1.6;margin-bottom:.8rem;">
                            {rep.get('description','—')}
                        </p>
                        <div style="display:flex;gap:1rem;flex-wrap:wrap;">
                            <div class="defect-meta-item" style="flex:1;min-width:140px;">
                                <div class="defect-meta-label">Cost Estimate</div>
                                <div class="defect-meta-value" style="color:#10B981;">
                                    {rep.get('cost_estimate_inr','—')}
                                </div>
                            </div>
                            <div class="defect-meta-item" style="flex:1;min-width:140px;">
                                <div class="defect-meta-label">Timeline</div>
                                <div class="defect-meta-value">{rep.get('timeline','—')}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("No repair recommendations generated.")

    # ── Download ───────────────────────────────────────────────────────────────
    st.markdown("<div class='glow-sep'></div>", unsafe_allow_html=True)
    json_str = json.dumps(r, indent=2)
    st.download_button(
        "⬇️ Download Crack Diagnostics Report (JSON)",
        data=json_str,
        file_name="crack_diagnostics_report.json",
        mime="application/json",
        key="crack_download",
    )
    with st.expander("🔍 View Raw JSON Report"):
        st.markdown(
            f"<div class='json-display'><pre>{json_str}</pre></div>",
            unsafe_allow_html=True,
        )
