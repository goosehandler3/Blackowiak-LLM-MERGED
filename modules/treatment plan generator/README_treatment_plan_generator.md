# 📋 Blackowiak LLM — Treatment Plan Generator Module

## Overview
This module adds a **Treatment Plan Generator** to the Blackowiak LLM. It produces clinically coherent, insurance-acceptable treatment plans based on structured inputs. Plans incorporate evidence-based modalities and can optionally include Internal Family Systems (IFS) language and trauma-informed framing.

---

## 🚀 Features
- **Diagnosis-Aligned Goal/Objective Builder** (ICD-10 compatible)
- **Modality-Specific Interventions** (CBT, DBT, EMDR, IFS, etc.)
- **Insurance-Ready Formatting**
- **Optional IFS/Parts Work Language**
- **SMART Objectives**
- **Client Strengths/Barriers Integration**
- **Export Formats**: `.docx`, `.pdf`, `.md`
- **Audit-Ready Metadata (optional)**

---

## 🧠 Input Schema
Example JSON input for the LLM prompt system:

```json
{
  "diagnoses": ["F33.1", "F41.1"],
  "focus_of_treatment": ["Anxiety", "Depression", "Trauma"],
  "modalities": ["DBT", "IFS"],
  "goals_requested": 3,
  "client_strengths": ["Motivated", "Insightful"],
  "client_barriers": ["History of substance use"],
  "session_frequency": "Biweekly",
  "format_style": "Insurance-Ready with Trauma Lens",
  "include_parts_work": true,
  "output_format": "markdown"
}
```

---

## 📄 Prompt Template
```jinja
You are a licensed mental health clinician creating a treatment plan for insurance and clinical use.

Diagnosis codes: {{ diagnoses }}
Treatment focus areas: {{ focus_of_treatment }}
Preferred modalities: {{ modalities }}
Client strengths: {{ client_strengths }}
Barriers to treatment: {{ client_barriers }}
Session frequency: {{ session_frequency }}
Include IFS-style language: {{ include_parts_work }}
Tone: {{ format_style }}

Generate:
- 3 goals with 2–3 SMART objectives each
- Interventions clearly tied to each goal and modality
- A structure that meets payer documentation expectations
```

---

## 🖥️ UI Integration

### Navigation
`Clients → Treatment Plan → [New Plan]`

### Controls
- ✅ Toggle: Include IFS/Parts Work
- ⬇️ Modalities Dropdown
- 🩺 Diagnosis Auto-Fill (ICD-10)
- 📄 Export Format Selector

---

## 🔐 Optional Compliance Features
- PHI Redaction Toggle
- Tamper-Proof Hashing (for versioned exports)
- Session metadata logging

---

## 📦 File Output
- `results/treatment_plan_<client_id>.md|pdf|docx`
- Redacted files saved with `_REDACTED` suffix if enabled
- Audit log (if enabled): `audit_logs/tp_export_<timestamp>.json`

---

## 🔧 Future Enhancements
- Integrated progress note generation synced to treatment plan goals
- LLM-assisted revision tool for 90-day updates
- Custom goal banks per diagnosis and modality

---

## ✅ Status
**[IN DEVELOPMENT]** — Backend logic complete. Front-end integration in progress.

To contribute or review code, see `/modules/treatment_plan_generator/`
