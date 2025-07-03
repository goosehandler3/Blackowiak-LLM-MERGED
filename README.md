# 🧠 Blackowiak LLM

**A HIPAA-aware local LLM pipeline for therapists, built by therapists.**  
Includes customizable note templates, AI-assisted summaries, voice support, and optional modes to fit your workflow (or mood).

---

## 🚀 Quick Start

```bash
# Clone and set up the environment
git clone https://github.com/yourusername/Blackowiak-LLM.git
cd Blackowiak-LLM
./setup.sh
python run.py --audio_path /path/to/audio.wav
```

> ⚠️ For Windows users: Use `setup_windows.py` instead.

---

## 🧩 Features

### 🎙️ Audio Pipeline
- Transcribes therapy sessions via Whisper
- Summarizes and generates notes with a local LLM (e.g., LLaMA3)
- Outputs include:
  - Full transcript
  - Session summary
  - BIRP / SOAP / EMDR / Psychoanalytic notes

### 🧠 Treatment Plan Generator
- Found under `modules/treatment plan generator/`
- Drafts treatment plans insurance will recognize
- Includes DBT, EMDR, and IFS-informed options

### 🗣️ Phrase Detection Module
- Detects key therapeutic phrases in transcripts
- Future support for tagging clinical risk language
- See `phrase_detection/README.md` for details

### 🎮 Themed Modes (Toggle at Runtime)
| Mode | Theme |
|------|-------|
| Sonic Mode | Speed + freedom |
| Plus Ultra Mode | Heroic + DBT-battle ready |
| Matrix Mode | Terminal-style clarity |
| Standalone Complex Mode | Cyberpunk therapy shell |
| Dream Mode | Fantasy-night calm |
| Insane Goofy Mode | 🤪 You’ve been warned |
| Michael Jackson Mode | Style + rhythm |

### 🖥️ Command Line Interface
- Optional CLI: `python app/cli.py`
- Supports file input, mode toggling, and batch runs

### 🛡️ Commercial + Privacy Tooling
- `license_manager.py`, `verify_privacy.py` for compliance
- `build.sh`, `excludes.txt` for bundle prep

---

## 📁 Folder Structure

```
Blackowiak-LLM/
├── app/                  # Core logic + modes
├── phrase_detection/     # Custom trigger detection (in development)
├── modules/              # Add-ons like treatment plan generator
├── output/               # Session files
├── templates/            # Note templates (BIRP, SOAP, etc.)
├── example_data/         # Sample files to test
├── docs/                 # Technical and usage docs
```

---

## ✍️ Templates Supported

- BIRP
- SOAP
- GIRP
- DAP
- EMDR Log
- Psychoanalytic Note

---

## 📄 Documentation

See the `docs/` folder for:
- `PROJECT_IMPLEMENTATION_SUMMARY.md`
- `FFMPEG_INSTALL.md`
- `DEVELOPMENT_ROADMAP.md`
- `LLM_CONTEXT_SUMMARY.md`
- `COMMERCIALIZATION_GUIDE.md`

---

## 👥 Credits

Created by Andrew Blackowiak, with contributions and experimental additions by Jeremy.
