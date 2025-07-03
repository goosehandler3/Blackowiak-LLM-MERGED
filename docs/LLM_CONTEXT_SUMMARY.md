# LLM CONTEXT SUMMARY
*For Use in New LLM Sessions*

## PROJECT OVERVIEW

**Name:** Blackowiak LLM - Professional Edition  
**Purpose:** Commercial, locally-run AI assistant for therapy session processing with advanced speaker diarization  
**Creator:** Andrew Blackowiak, MSW - Athens, GA Therapist, Technologist, Millennial Futurist  
**License:** Commercial (License-Protected)  
**Target Users:** Professional therapists, clinical professionals, private practice owners  
**Distribution:** macOS commercial binary with DMG installer, license activation system  

## CORE PHILOSOPHY

This is not just a tool—it's a paradigm shift. The project exists at the intersection of trauma-informed care, psychedelic therapy, existential inquiry, and leftist clinical ethics. It's designed for the next generation of therapists who understand rhythm, cybernetics, and full narrative integration. The system is built with clinical defensibility, privacy-first design, and local processing to ensure no client data ever leaves the therapist's computer.

**Commercial Evolution:** The project has evolved from open-source to a professional commercial product with license protection, advanced diarization capabilities, and a complete build/distribution system for macOS. It maintains its core privacy-first philosophy while adding enterprise-grade features and customer support systems.

## TECHNICAL ARCHITECTURE

### Core Components
1. **Advanced Audio Processing Pipeline** (`app/core.py`)
   - OpenAI Whisper for speech-to-text transcription (**100% local**)
   - **Advanced neural speaker diarization** using pyannote.audio (**100% local**)
   - **LLM-enhanced speaker role assignment** for therapist/client identification (**100% local**)
   - **Multiple diarization modes:** simple (pause-based), advanced (neural), enhanced (LLM)
   - Support for WAV, MP3, M4A audio formats
   - Handles long audio files with proper chunking
   - Graceful fallback between diarization methods
   - **All processing happens on local machine - no cloud APIs**

2. **Local LLM Integration**
   - Uses Ollama for completely local processing (no cloud APIs)
   - Generates therapy session summaries
   - Creates SOAP format clinical notes
   - **LLM post-processing** for speaker role refinement
   - Supports multiple LLM models (llama3.2 recommended)

3. **Enhanced CLI Interface** (`run.py`)
   - Simple command-line interface with advanced options
   - Multiple Whisper model options (tiny, base, small, medium, large)
   - **Advanced diarization toggle** (--basic-mode, --no-llm-enhancement)
   - Configurable output directories
   - Rich CLI output with progress bars
   - **License activation and validation** (--activate-license)

4. **Commercial License System** (`license_manager.py`)
   - **Hardware-bound license activation** with machine fingerprinting
   - **Usage tracking and enforcement** (trial limits, expiration dates)
   - **Multiple license types:** trial, standard, professional
   - **Vendor tools** for license generation and management
   - **CLI license management** (activate, status, validate)
   - **Offline license validation** after initial activation

5. **Advanced Build System** (`build_advanced.sh`)
   - **macOS-only commercial build pipeline** with PyInstaller
   - **DMG installer creation** with professional packaging
   - **Build caching system** for faster development iterations
   - **Customer package preparation** with documentation
   - **Vendor tool distribution** for license management

### Key Dependencies
- **Audio:** `openai-whisper`, `torch`, `torchaudio`, `librosa`, `pydub`
- **LLM:** `ollama`, `requests`
- **CLI:** `click`, `rich`
- **Advanced Diarization:** `pyannote.audio`, `speechbrain` (included in commercial build)
- **License System:** `cryptography`, `psutil`, `platform` (hardware binding)
- **Build System:** `pyinstaller`, `dmgbuild` (macOS distribution)
- **Optional:** `presidio-analyzer` (PHI redaction), `huggingface-hub` (model access)

## CURRENT STATE (COMMERCIAL READY)

### ✅ Working Features
- **Audio Transcription:** Converts therapy session audio to text using OpenAI Whisper
- **Advanced Speaker Diarization:** Neural speaker identification with pyannote.audio
- **LLM-Enhanced Speaker Roles:** Uses Ollama to intelligently assign therapist/client roles
- **Multiple Diarization Methods:** Simple (pause-based), advanced (neural), and LLM-enhanced
- **Local LLM Processing:** Complete local generation of summaries and clinical notes
- **Multiple Output Formats:** Transcript, summary, SOAP note, JSON data
- **macOS Commercial Distribution:** PyInstaller binary + DMG installer
- **License Protection System:** Hardware-bound activation, usage tracking, trial/commercial licenses
- **Privacy Focused:** All processing happens locally (no cloud APIs)
- **Graceful Fallbacks:** System degrades gracefully when advanced features unavailable
- **Build Caching:** Fast iteration for development and testing
- **Customer Onboarding:** Professional installer, documentation, quick start guides

### 🚀 Setup & Installation
1. **Prerequisites:** Python 3.12.11, ffmpeg, Ollama
2. **Development:** Automated via `setup.sh` script + `installer.py` (enhanced)
3. **Commercial:** DMG installer with guided setup wizard
4. **Verification:** `test_installation.py` + `test_commercial_readiness.py`
5. **Demo:** `create_demo.py` generates test materials
6. **License:** Activation required for commercial builds

### 📁 Project Structure
```
/
├── README.md                    # Main project documentation
├── QUICK_START.md              # Complete setup guide for new users
├── run.py                      # Main launcher script (with license integration)
├── setup.sh                    # Automated installation script
├── installer.py                # Enhanced commercial installer
├── requirements.txt            # Core dependencies
├── requirements-advanced.txt   # Advanced diarization dependencies
├── requirements-legacy.txt     # Legacy Python support
├── test_installation.py        # Dependency verification
├── test_commercial_readiness.py # Commercial build validation
├── create_demo.py             # Demo material generation
├── check_asdf.sh              # Python version verification
├── .tool-versions             # ASDF Python version (3.12.11)
├── license_manager.py         # Commercial license system
├── build_advanced.sh          # macOS commercial build script (with caching)
├── app/
│   ├── core.py                # Main processing engine (license-protected)
│   └── modes/                 # Future feature modes
├── templates/                 # Clinical note templates
├── docs/                      # Comprehensive documentation
│   ├── COMMERCIALIZATION_GUIDE.md
│   ├── LAUNCH_CHECKLIST.md
│   ├── FINAL_LAUNCH_SUMMARY.md
│   ├── CUSTOMER_README.md
│   ├── QUICK_START_CARD.md
│   ├── DEPENDENCY_GUIDE.md
│   └── [other docs]
├── example_data/              # Test data and examples
├── output/                    # Generated files directory
└── .gitignore                # Excludes PHI, cache, audio logs, licenses
```

## DEVELOPMENT ROADMAP

### Phase 1: Core Functionality (✅ COMPLETE)
- Audio processing pipeline
- Local LLM integration
- Basic CLI interface
- SOAP note generation

### Phase 2: Advanced Processing & Commercial Foundation (✅ COMPLETE)
- Advanced speaker diarization with pyannote.audio
- License management and activation system
- macOS commercial build pipeline with PyInstaller
- Customer onboarding and documentation
- Build caching and optimization

### Phase 3: Market Launch & Expansion (� NEXT)
- DMG distribution and customer acquisition
- Payment processing integration
- Customer support systems
- Performance optimization and testing

### Phase 4: Advanced Features (� PLANNED)
- PHI redaction with Presidio
- Multiple clinical note formats
- Confidence scoring and quality metrics
- Real-time processing capabilities

### Phase 5: Platform Expansion (🔮 FUTURE)
- Windows and Linux commercial builds
- GUI desktop application
- "Modes": Sonic Mode, Plus Ultra, Dream Mode, Matrix Mode
- Template customization interface

### Phase 6: Clinical Integration (🎯 VISION)
- EHR integration
- Automated billing codes
- Outcome tracking
- Supervision tools and compliance features

## USAGE PATTERNS

### Commercial Usage (Recommended)
```bash
# License activation (first time)
./blackowiak-llm-1.0.0 --activate-license YOUR_LICENSE_CODE

# Check license status
./blackowiak-llm-1.0.0 --license-status

# Process therapy session
./blackowiak-llm-1.0.0 your_audio_file.wav

# Advanced processing with large model
./blackowiak-llm-1.0.0 --whisper-model large your_audio_file.wav
```

### Development Usage
```bash
# Setup (first time)
chmod +x setup.sh && ./setup.sh
source venv/bin/activate
python test_installation.py

# Basic processing
python run.py your_audio_file.wav

# Advanced processing (default)
python run.py --whisper-model medium your_audio_file.wav

# Basic mode (disable advanced features)
python run.py --basic-mode your_audio_file.wav

# License testing (development)
python run.py --activate-license DEMO_LICENSE_CODE
```

### Advanced Setup (for Neural Diarization)
```bash
# Install advanced dependencies (development)
pip install -r requirements-advanced.txt

# Commercial builds include advanced features by default

# Get Hugging Face token for pyannote models
# 1. Create account at https://huggingface.co/
# 2. Get token at https://huggingface.co/settings/tokens
# 3. Set environment variable
export HF_TOKEN="your_token_here"

# Test advanced features
python run.py --verbose your_audio_file.wav
```

### Build System Usage
```bash
# Build macOS commercial binary
./build_advanced.sh binary

# Build complete commercial package
./build_advanced.sh all

# Create DMG installer
./build_advanced.sh dmg

# Vendor tools for license management
./build_advanced.sh vendor

# Cache management
./build_advanced.sh cache-info
./build_advanced.sh clean-cache
```

### Output Files Generated
- `transcript_YYYYMMDD_HHMMSS.txt` - Raw transcript with speaker labels
- `summary_YYYYMMDD_HHMMSS.txt` - Therapeutic session summary
- `soap_note_YYYYMMDD_HHMMSS.txt` - Clinical SOAP format note
- `session_data_YYYYMMDD_HHMMSS.json` - Complete session data

## SECURITY & PRIVACY

- **100% Local-First:** All processing happens on local machine (audio, transcription, diarization, LLM)
- **No Cloud APIs:** Uses Ollama + pyannote.audio, not OpenAI/Anthropic/cloud services
- **PHI Protection:** Designed for clinical data handling with local-only processing
- **License Security:** Hardware-bound activation with cryptographic validation
- **Audit Trail:** Session logs and processing history stored locally
- **Template Security:** Customizable clinical note templates
- **Model Downloads:** One-time setup downloads models to local cache (HF token for access only)
- **Offline Capable:** Fully functional without internet after initial setup and license activation
- **Commercial Grade:** Enterprise-level security with usage tracking and compliance features

## TECHNICAL NOTES FOR LLMS

### Code Quality
- **Modular Design:** Separation of concerns between audio, LLM, and CLI
- **Error Handling:** Comprehensive error checking and user feedback
- **Rich CLI:** Progress bars, colored output, clear status messages
- **Cross-Platform:** Works on macOS, Linux, Windows with proper dependencies

### Common Issues & Solutions
- **ffmpeg Missing:** Install via Homebrew/apt/chocolatey
- **Python Version:** Requires 3.10+ (3.12.11 recommended via ASDF)
- **Memory Issues:** Adjustable Whisper model sizes (tiny to large)
- **Audio Formats:** Supports most common formats, converts internally

### Extension Points
- **New Clinical Templates:** Add to `templates/` directory
- **Custom LLM Prompts:** Modify prompts in `app/core.py`
- **Audio Processing:** Extend AudioProcessor class
- **Output Formats:** Add new output generators
- **License Types:** Extend license system in `license_manager.py`
- **Build Targets:** Add new platforms to `build_advanced.sh`

## ONBOARDING PATHS

### For Professional Therapists (Commercial Users)
1. Download DMG installer from website
2. Run professional installer with guided setup
3. Activate license with provided license code
4. Follow `QUICK_START_CARD.md` for first session
5. Use `CUSTOMER_README.md` for ongoing reference

### For Therapists (Development/Testing)
1. Start with `QUICK_START.md`
2. Follow automated setup via `setup.sh`
3. Use `create_demo.py` for test materials
4. Process first audio file with basic commands

### For Technical Users (SREs, Developers)
1. Review `docs/PROJECT_IMPLEMENTATION_SUMMARY.md`
2. Examine `app/core.py` and `license_manager.py` for architecture
3. Run `test_installation.py` and `test_commercial_readiness.py`
4. Explore build system with `build_advanced.sh`
5. Check `docs/COMMERCIALIZATION_GUIDE.md` for business logic

## DOCUMENTATION HIERARCHY

1. **Entry Points:**
   - `README.md` - Project overview and quick navigation
   - `QUICK_START.md` - Complete setup for new Mac users

2. **Technical Documentation:**
   - `docs/PROJECT_IMPLEMENTATION_SUMMARY.md` - What's built
   - `docs/DEVELOPMENT_ROADMAP.md` - 5-phase development plan
   - `docs/TROUBLESHOOTING.md` - Problem-solving guide

3. **Setup & Installation:**
   - `setup.sh` - Automated development installation
   - `installer.py` - Enhanced commercial installer with dependency checking
   - `docs/FFMPEG_INSTALL.md` - Manual ffmpeg setup
   - `test_installation.py` - Dependency verification
   - `test_commercial_readiness.py` - Commercial build validation

4. **Commercial & Customer:**
   - `docs/COMMERCIALIZATION_GUIDE.md` - Business implementation guide
   - `docs/LAUNCH_CHECKLIST.md` - Pre-launch validation
   - `docs/FINAL_LAUNCH_SUMMARY.md` - Launch readiness summary
   - `CUSTOMER_README.md` - Customer-facing documentation
   - `QUICK_START_CARD.md` - Quick reference for daily use
   - `DEPENDENCY_GUIDE.md` - Dependency installation guide

5. **Advanced:**
   - `docs/CONTRIBUTING.md` - Development guidelines
   - `app/core.py` - Main implementation (license-protected)
   - `license_manager.py` - Commercial license system
   - `build_advanced.sh` - macOS build pipeline with caching

## CONTEXT FOR NEW LLM SESSIONS

When starting a new LLM session about this project:

1. **Current State:** Commercial product ready for market launch
2. **Architecture:** Local audio processing → Whisper → pyannote.audio → Ollama → Clinical notes
3. **Key Files:** `app/core.py` (main engine), `license_manager.py` (licensing), `build_advanced.sh` (build system)
4. **Dependencies:** Python 3.12.11, ffmpeg, Ollama, Whisper, pyannote.audio
5. **Target Users:** Professional therapists, private practice owners
6. **Philosophy:** Privacy-first, local processing, commercial-grade quality
7. **Development:** Well-documented, modular, license-protected codebase
8. **Distribution:** macOS-focused with DMG installer and professional onboarding
9. **License System:** Hardware-bound activation with trial/commercial tiers
10. **Build System:** Advanced caching, automated packaging, customer-ready distribution

The project has evolved from open-source MVP to commercial-ready product with enterprise features, license protection, and professional distribution systems.
