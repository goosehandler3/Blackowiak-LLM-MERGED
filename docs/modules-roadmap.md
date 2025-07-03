# 🛠 Module Roadmap for Blackowiak LLM

This roadmap outlines the development priorities and projected functionality for the major components of Blackowiak LLM. Each module is designed to enhance offline clinical documentation, insight generation, and legal defensibility.

---

## ✅ Already Prototyped

### `templates/`
- SOAP, BIRP, DAP, GIRP
- EMDR session logging
- Psychoanalytic note format

### `example_data/`
- Fake `.ics` calendar file
- Sample session notes (with/without PHI)

---

## 🚧 Core Modules (Under Development)

### `app/gui/`
- [ ] Tab-based GUI with Sonic toggle
- [ ] Client note browser & calendar view
- [ ] Session note generator and editor
- [ ] Data vault for backups + audit review

### `app/llm/`
- [ ] Local inference with Ollama, Mistral, or Phi
- [ ] Embedding + retrieval system for longitudinal recall
- [ ] Prompt chaining: calendar > redactor > summarizer > plan

### `app/redactor/`
- [x] Regex-based PHI redaction and aliasing
- [ ] Fuzzy detection + optional manual review
- [ ] Presidio or spaCy pipeline fallback

### `app/calendar/`
- [x] Parses `.ics` from SimplePractice
- [ ] Links events to client aliases
- [ ] Suggests gaps, trends, no-shows, etc.

### `app/voice/`
- [ ] Piper TTS (Jarvis, Steve Irwin, etc.)
- [ ] Whisper transcription from mic or file
- [ ] Diarization and speaker labeling

---

## 💡 Future Add-Ons

- `modules/insight_engine/`: Suggests interventions based on past sessions
- `modules/group_view/`: Handles group therapy tracking
- `modules/rhythm_analytics/`: Client mood/energy patterns over time
- `modules/psychedelic_journal/`: Integration logs with alternate formatting

---

This roadmap evolves with each sprint. Blackowiak LLM is not a static tool—it’s a self-reflective assistant for the therapeutic process, shaped by the rhythms of clinical life.
