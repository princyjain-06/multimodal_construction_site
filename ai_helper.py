"""
Gemini AI helper module — uses the new `google-genai` SDK.
Provides a unified interface for text + vision calls with graceful demo fallback.
"""

from __future__ import annotations
import json, re, textwrap, io
from typing import Optional
from PIL import Image


# ─── Model candidates (tried in order until one works) ─────────────────────────
_MODEL_CANDIDATES = [
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
]

_CACHED_WORKING_MODELS: dict[str, str] = {}


# ─── Gemini Client ─────────────────────────────────────────────────────────────

def _get_client(api_key: str):
    """Return a configured google-genai Client, or None if key missing."""
    clean_key = (api_key or "").strip()
    if not clean_key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=clean_key)
    except Exception:
        return None


def _find_working_model(client, api_key: str) -> str:
    """
    Find and return the best available model name for this client.
    Caches the result to avoid redundant probing requests.
    """
    clean_key = (api_key or "").strip()
    if clean_key in _CACHED_WORKING_MODELS:
        return _CACHED_WORKING_MODELS[clean_key]

    # 1. Try listing models from the API
    try:
        available = []
        for m in client.models.list():
            name = getattr(m, "name", "")
            if name.startswith("models/"):
                name = name[7:]
            available.append(name)
        for cand in _MODEL_CANDIDATES:
            if cand in available:
                _CACHED_WORKING_MODELS[clean_key] = cand
                return cand
        for m in available:
            if "gemini" in m.lower() and "flash" in m.lower():
                _CACHED_WORKING_MODELS[clean_key] = m
                return m
    except Exception:
        pass

    # 2. Try pinging candidates
    try:
        from google.genai import types as genai_types
        for model_name in _MODEL_CANDIDATES:
            try:
                client.models.generate_content(
                    model=model_name,
                    contents="hi",
                    config=genai_types.GenerateContentConfig(max_output_tokens=1),
                )
                _CACHED_WORKING_MODELS[clean_key] = model_name
                return model_name
            except Exception:
                continue
    except Exception:
        pass

    # Default to modern 3.8 flash so specific API errors can surface cleanly
    return _MODEL_CANDIDATES[0]


def call_gemini_vision(api_key: str, prompt: str, image: Image.Image) -> str:
    """Send a multimodal (text + image) request to Gemini."""
    clean_key = (api_key or "").strip()
    client = _get_client(clean_key)
    if client is None:
        return "__ERROR__: No API key provided."

    model_name = _find_working_model(client, clean_key)

    try:
        from google.genai import types as genai_types

        # Convert PIL Image → bytes
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        image_bytes = buf.getvalue()

        response = client.models.generate_content(
            model=model_name,
            contents=[
                genai_types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                prompt,
            ],
        )
        return response.text
    except Exception as exc:
        return f"__ERROR__: {exc}"


def call_gemini_text(api_key: str, prompt: str) -> str:
    """Send a text-only request to Gemini."""
    clean_key = (api_key or "").strip()
    client = _get_client(clean_key)
    if client is None:
        return "__ERROR__: No API key provided."

    model_name = _find_working_model(client, clean_key)

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text
    except Exception as exc:
        return f"__ERROR__: {exc}"


def extract_json_from_response(text: str) -> Optional[dict]:
    """
    Extract the first JSON object found in the model response.
    Returns None on failure.
    """
    # Strip markdown fences
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`")
    # Find outermost { ... }
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


# ─── Demo / Fallback Data ──────────────────────────────────────────────────────

DEMO_SAFETY_RESULT = {
    "safety_score": 74,
    "overall_status": "Moderate Risk",
    "ppe_detection": {
        "helmets": {"status": "Compliant", "detected": True, "workers_wearing": 8, "total_workers": 9},
        "high_vis_vests": {"status": "Non-Compliant", "detected": False, "workers_wearing": 5, "total_workers": 9},
        "steel_toe_boots": {"status": "Compliant", "detected": True, "workers_wearing": 9, "total_workers": 9},
        "safety_harnesses": {"status": "Non-Compliant", "detected": False, "workers_wearing": 0, "total_workers": 3},
        "safety_glasses": {"status": "Partial", "detected": True, "workers_wearing": 4, "total_workers": 6},
    },
    "site_hazards": [
        {
            "hazard": "Workers at height without safety harnesses",
            "severity": "Critical",
            "osha_ref": "OSHA 1926.502",
            "remedy": "Immediately halt elevated work. Enforce fall-arrest system for all workers above 1.8 m. Conduct toolbox talk before resuming.",
        },
        {
            "hazard": "Missing high-visibility vests in active vehicle zone",
            "severity": "High",
            "osha_ref": "OSHA 1926.201",
            "remedy": "Issue ANSI Class 2 vests to all workers in the traffic/equipment zone. Station a spotter near heavy machinery.",
        },
        {
            "hazard": "Unsecured scaffolding components on upper deck",
            "severity": "Medium",
            "osha_ref": "OSHA 1926.451",
            "remedy": "Secure all scaffold planks with locking pins. Conduct daily scaffold inspection before shift start.",
        },
        {
            "hazard": "Electrical cable runs across pedestrian walkway",
            "severity": "Low",
            "osha_ref": "OSHA 1926.416",
            "remedy": "Route cables through conduit or overhead tray. Place rubber cable protectors at crossing points.",
        },
    ],
    "standard": "OSHA 29 CFR 1926 / IS 456:2000",
    "inspection_timestamp": "2026-10-28T09:51:07+05:30",
}

DEMO_CRACK_RESULT = {
    "defect_type": "Structural Shear Crack",
    "crack_width_mm": 2.4,
    "crack_length_mm": 340,
    "orientation": "Diagonal (45°)",
    "urgency": "High – Immediate Engineering Review Required",
    "root_causes": [
        "Excess shear stress exceeding concrete tensile capacity",
        "Inadequate shear reinforcement spacing (>150 mm c/c)",
        "Possible differential settlement of foundation",
        "Construction joint poorly treated during pour",
    ],
    "recommended_repairs": [
        {
            "method": "Epoxy Injection",
            "description": "High-pressure epoxy resin injection to seal and restore structural continuity. Suitable for cracks > 0.2 mm.",
            "cost_estimate_inr": "₹18,000 – ₹35,000 per linear metre",
            "timeline": "2–4 days",
        },
        {
            "method": "Structural Re-grouting",
            "description": "Cement-based polymer grout injected under pressure. Suitable where crack extends to reinforcement.",
            "cost_estimate_inr": "₹12,000 – ₹22,000 per linear metre",
            "timeline": "3–5 days",
        },
        {
            "method": "Carbon Fibre Reinforced Polymer (CFRP) Wrap",
            "description": "External bonded CFRP strips applied perpendicular to crack for additional shear capacity.",
            "cost_estimate_inr": "₹45,000 – ₹90,000 per panel",
            "timeline": "4–7 days",
        },
    ],
    "is_standard_ref": "IS 456:2000 Clause 26.5.1 — Shear Reinforcement",
    "structural_risk": "Moderate-High",
}


def build_safety_prompt() -> str:
    return textwrap.dedent("""
        You are a certified construction site safety inspector trained in OSHA 29 CFR 1926 and IS 456:2000.
        Analyze the uploaded construction site photo and produce a JSON response with EXACTLY this structure:

        {
          "safety_score": <integer 0-100>,
          "overall_status": "<Safe | Low Risk | Moderate Risk | High Risk | Critical>",
          "ppe_detection": {
            "helmets":          {"status":"<Compliant|Non-Compliant|Partial>","detected":<bool>,"workers_wearing":<int>,"total_workers":<int>},
            "high_vis_vests":   {"status":"<Compliant|Non-Compliant|Partial>","detected":<bool>,"workers_wearing":<int>,"total_workers":<int>},
            "steel_toe_boots":  {"status":"<Compliant|Non-Compliant|Partial>","detected":<bool>,"workers_wearing":<int>,"total_workers":<int>},
            "safety_harnesses": {"status":"<Compliant|Non-Compliant|Partial>","detected":<bool>,"workers_wearing":<int>,"total_workers":<int>},
            "safety_glasses":   {"status":"<Compliant|Non-Compliant|Partial>","detected":<bool>,"workers_wearing":<int>,"total_workers":<int>}
          },
          "site_hazards": [
            {
              "hazard":   "<description>",
              "severity": "<Low|Medium|High|Critical>",
              "osha_ref": "<OSHA clause>",
              "remedy":   "<corrective action>"
            }
          ],
          "standard": "OSHA 29 CFR 1926 / IS 456:2000",
          "inspection_timestamp": "<ISO 8601>"
        }

        Return ONLY the JSON object. No markdown, no explanation.
    """).strip()


def build_crack_prompt() -> str:
    return textwrap.dedent("""
        You are a structural engineering expert specializing in concrete defect analysis per IS 456:2000.
        Analyze the uploaded image of a concrete/wall surface and return ONLY a JSON object with this structure:

        {
          "defect_type": "<Hairline|Settlement|Structural Shear|Thermal Expansion|Spalling|Other>",
          "crack_width_mm": <float>,
          "crack_length_mm": <float>,
          "orientation": "<Vertical|Horizontal|Diagonal|Random>",
          "urgency": "<Low – Monitor|Medium – Plan Repair|High – Immediate Engineering Review Required|Critical – Evacuate>",
          "root_causes": ["<cause1>", "<cause2>"],
          "recommended_repairs": [
            {
              "method": "<method name>",
              "description": "<details>",
              "cost_estimate_inr": "<range>",
              "timeline": "<duration>"
            }
          ],
          "is_standard_ref": "<IS clause>",
          "structural_risk": "<Low|Moderate|Moderate-High|High|Critical>"
        }

        Return ONLY the JSON object. No markdown, no explanation.
    """).strip()
