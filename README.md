# Multimodal Construction Intelligence Platform

> **Skill Wallet Capstone Project 1** | Powered by Google Gemini 2.0 Flash | OSHA & IS 456 Compliant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-orange)](https://aistudio.google.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🏗️ Overview

A production-ready multimodal AI platform for construction intelligence, featuring:

| Module | Epic | Description |
|--------|------|-------------|
| 🦺 Site Safety & PPE Audit | Epic 2 | OSHA/IS 456 PPE compliance via Gemini Vision |
| 🔬 Crack Diagnostics | Epic 2 | Structural defect classification & repair recommendations |
| 📐 Planning & Valuation | Epic 3 | INR budget, CapEx, market valuation & 3D renders |
| 🤖 Site Assistant | Epic 5 | Weather-aware alerts & multi-turn engineering chatbot |

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/princyjain-06/multimodal_construction_site.git
cd multimodal_construction_site
pip install -r requirements.txt
```

### 2. Run
```bash
streamlit run app.py
```

### 3. API Key
Get your free Google Gemini API key at **[aistudio.google.com](https://aistudio.google.com)**  
Enter it in the sidebar — or use **Demo Mode** without any key.

---

## 📦 Project Structure

```
Multimodal-project/
├── app.py              # Main entry point
├── styles.py           # Custom CSS (dark-mode amber theme)
├── sidebar.py          # Sidebar: API key, architecture, navigation
├── ai_helper.py        # Gemini Vision/Text API + demo fallbacks
├── tab_safety.py       # Tab 1: PPE & Hazard Audit
├── tab_crack.py        # Tab 2: Crack Diagnostics
├── tab_valuation.py    # Tab 3: Project Planning & Valuation
├── tab_assistant.py    # Tab 4: Weather Advisory + Chatbot
├── requirements.txt    # Python dependencies
└── .streamlit/
    └── config.toml     # Streamlit theme & server config
```

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set **Main file** to `app.py`
4. Add `GOOGLE_API_KEY` as a secret (optional)
5. Click **Deploy** ✅

---

## 🛡️ Standards Referenced

- **OSHA 29 CFR 1926** — Construction Industry Safety Standards
- **IS 456:2000** — Plain and Reinforced Concrete
- **IS 13920** — Ductile Detailing of RC Structures  
- **NBC 2016** — National Building Code of India

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| UI Framework | Streamlit |
| AI Vision + Chat | Google Gemini 2.0 Flash |
| 3D Renders | Pollinations AI |
| Charts | Plotly |
| Image Processing | Pillow |
| Language | Python 3.10+ |
| Deployment | Streamlit Community Cloud |

---

## 📄 License

MIT License — Free to use, modify, and distribute.
