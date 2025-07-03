# Documentation: Blackowiak LLM

This is the development-level design documentation for Blackowiak LLM.

---

## 📦 Module Overview

### `app/gui/`
Handles the user interface, navigation, and session interaction.
- Planned: Tkinter or PyQt GUI
- Optional: Sonic Mode toggle, visual themes

### `app/llm/`
Logic for interfacing with the local language model.
- Hooks for prompt formatting and response parsing
- Will integrate with Ollama or another local engine

### `app/voice/`
Handles TTS output and Whisper-based transcription.
- Placeholder for Piper output
- Optional: Diarization for speaker separation
- Includes toggleable interruption mode

### `app/redactor/`
Automated redaction using regex-based PHI detection.
- Replaces PHI with tags (e.g., `[NAME]`, `[DATE]`)
- Flags uncertain items for human review

### `app/calendar/`
Parses `.ics` files from SimplePractice or other EHRs.
- Maps calendar data to client aliases
- Optional: Track session frequency, duration, etc.

---

## 📝 Note Templates

Located in `templates/`:
- SOAP, BIRP, DAP, GIRP
- EMDR session logs
- Psychoanalytic notes

---

## 🧪 Example Data

Located in `example_data/`:
- Fake session notes
- Demo `.ics` file

---

## 🚀 Quick Start

```bash
python run.py
```

Dependencies:
```bash
pip install -r requirements.txt
```

---

This project is under active development and intended for local use only. Not for production until further review and legal vetting.
