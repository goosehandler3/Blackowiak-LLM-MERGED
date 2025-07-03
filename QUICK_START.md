# QUICK START GUIDE

This guide will help you get the Blackowiak LLM system up and running on a **brand new Mac** to process therapy session audio files. We'll start from the very beginning and walk through every step.

## 🍎 New Mac Setup (Start Here!)

If you're setting up a brand new Mac or haven't done development before, follow these foundational steps:

### Step 1: Install Xcode Command Line Tools

Many terminal operations will prompt you to install these, so let's get them out of the way first:

```bash
xcode-select --install
```

This will open a dialog box. Click "Install" and wait for it to complete (this can take 10-30 minutes).

### Step 2: Install Homebrew (Package Manager)

Homebrew lets you install developer tools easily. Open Terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Important**: After installation, Homebrew will show you commands to add it to your PATH. Copy and run those commands! They'll look something like:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Verify Homebrew is working:
```bash
brew --version
```

### Step 3: Install ASDF (Version Manager)

ASDF helps manage different versions of programming languages. This project uses Python 3.12.11 as specified in the `.tool-versions` file.

```bash
# Install ASDF
brew install asdf

# Add ASDF to your shell (choose your shell)
# For zsh (default on new Macs):
echo '. /opt/homebrew/opt/asdf/libexec/asdf.sh' >> ~/.zshrc

# For bash:
echo '. /opt/homebrew/opt/asdf/libexec/asdf.sh' >> ~/.bash_profile

# Restart your terminal or run:
source ~/.zshrc  # or source ~/.bash_profile for bash
```

### Step 4: Install Python via ASDF

```bash
# Add Python plugin to ASDF
asdf plugin add python

# Install the specific Python version for this project
asdf install python 3.12.11

# Set it as the default
asdf global python 3.12.11

# Verify Python installation
python3 --version  # Should show Python 3.12.11
```

### Step 5: Install ffmpeg (Required for Audio Processing)

```bash
brew install ffmpeg

# Verify installation
ffmpeg -version
```

## 📁 Project Setup

Now that your Mac is set up for development, let's get the project running:

### Step 1: Get the Project

```bash
# Navigate to where you want the project (e.g., Desktop)
cd ~/Desktop

# Clone the project (replace with actual repo URL)
git clone https://github.com/yourusername/blackowiak-llm.git
cd blackowiak-llm

# The .tool-versions file will automatically use Python 3.12.11
# Verify you're using the right Python version:
python3 --version

# Optional: Run our verification script
./check_asdf.sh
```

### Step 2: Set Up the Environment

```bash
# Make the setup script executable
chmod +x setup.sh

# Run the automated setup
./setup.sh
```

This script will:
- Create a Python virtual environment
- Install all required packages
- Check for system dependencies

### Step 3: Install Local LLM (Ollama)

Download and install Ollama from [ollama.ai](https://ollama.ai/):

1. **Download**: Go to https://ollama.ai/ and download for macOS
2. **Install**: Open the downloaded file and drag Ollama to Applications
3. **Launch**: Open Ollama from Applications (it will run in the background)
4. **Download a model**:
   ```bash
   ollama pull llama3.2
   ```

### Step 4: Test Everything Works

```bash
# Activate the virtual environment
source venv/bin/activate

# Run the installation test
python test_installation.py
```

You should see all green checkmarks ✅. If you see any red X marks ❌, check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide.

### Step 5: Create Demo Materials

```bash
# Generate example files for testing
python create_demo.py
```

This creates sample transcripts and instructions for creating test audio.

## 🎵 Processing Your First Audio File

### Create Test Audio

Since we can't include real therapy recordings, you'll need to create test audio:

**Option 1: Use macOS Text-to-Speech**
```bash
# Create a simple test file
say -v Alex -o test_therapist.wav "Hello, how are you feeling today?"
say -v Samantha -o test_client.wav "I'm feeling anxious about work."

# Combine them (you can use audio editing software or just test with one)
```

**Option 2: Record Yourself**
- Open QuickTime Player
- File → New Audio Recording
- Record yourself reading the demo transcript
- Save as a .wav file

### Process the Audio

```bash
# Make sure virtual environment is active
source venv/bin/activate

# Process your audio file
python run.py your_audio_file.wav

# Or with more options:
python run.py audio.wav --whisper-model medium --output results/
```

### Check the Results

Look in the `output/` directory (or whatever you specified) for:
- **transcript_YYYYMMDD_HHMMSS.txt**: Raw transcript with speaker labels
- **summary_YYYYMMDD_HHMMSS.txt**: Session summary
- **soap_note_YYYYMMDD_HHMMSS.txt**: SOAP format clinical note
- **session_data_YYYYMMDD_HHMMSS.json**: Complete data in JSON format

## 🎛️ Advanced Options

### Command Line Options

```bash
# Use different Whisper models (trade speed vs accuracy)
python run.py audio.wav --whisper-model tiny     # Fastest
python run.py audio.wav --whisper-model base     # Default
python run.py audio.wav --whisper-model medium   # Better accuracy
python run.py audio.wav --whisper-model large    # Best accuracy

# Specify output directory
python run.py audio.wav --output /path/to/results

# Use different LLM model
python run.py audio.wav --llm-model codellama

# Enable verbose logging
python run.py audio.wav --verbose
```

### Speaker Diarization Options

The system offers three levels of speaker identification:

```bash
# Simple diarization (default) - fast, based on speech pauses
python run.py audio.wav --diarization simple

# Advanced diarization - AI-powered, most accurate
python run.py audio.wav --diarization advanced

# LLM-enhanced diarization - uses AI to improve speaker identification
python run.py audio.wav --diarization llm-enhanced
```

**Advanced Diarization Features**:
- More accurate speaker identification
- Better handling of overlapping speech
- Improved separation of multiple speakers
- All processing remains local and private

**Requirements for Advanced Diarization**:
- Hugging Face token (free, see setup above)
- Additional ~500MB for AI models (downloaded once)
- Requires `pip install -r requirements-advanced.txt`

### Working with Real Audio Files

The system works with:
- ✅ WAV files (best)
- ✅ MP3 files
- ✅ M4A files
- ✅ Most common audio formats

For best results:
- Clear audio with minimal background noise
- Session length: 15 minutes to 2+ hours
- Two speakers (therapist and client)

### Step 6: Optional Advanced Speaker Diarization Setup

For more accurate speaker identification, especially in complex audio with multiple speakers or overlapping speech, you can enable advanced speaker diarization:

**What it does**: Uses AI models to precisely identify who is speaking when, creating more accurate clinical notes.

**Privacy guarantee**: All processing happens locally on your Mac. No audio is ever uploaded to external servers. The Hugging Face token is only used to download models to your computer.

```bash
# Install advanced diarization dependencies
pip install -r requirements-advanced.txt
```

**Get a Hugging Face Token** (free and only used for model downloads):

1. Go to [huggingface.co](https://huggingface.co/) and create a free account
2. Go to Settings → Access Tokens
3. Create a new token with "Read" permissions
4. Accept the pyannote/segmentation-3.0 model terms at:
   - https://huggingface.co/pyannote/segmentation-3.0
   - https://huggingface.co/pyannote/speaker-diarization-3.1

**Set up your token**:
```bash
# Option 1: Set environment variable (recommended)
export HUGGING_FACE_HUB_TOKEN="your_token_here"

# Option 2: Or add to your shell profile for permanent setup
echo 'export HUGGING_FACE_HUB_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

**Test advanced diarization**:
```bash
# Verify privacy (shows all processing is local)
python verify_privacy.py

# Process audio with advanced diarization
python run.py audio.wav --diarization advanced
```

**Note**: The first time you use advanced diarization, it will download AI models (~500MB). This happens once and then everything runs offline.

For complete privacy details and troubleshooting, see [docs/ADVANCED_DIARIZATION_GUIDE.md](docs/ADVANCED_DIARIZATION_GUIDE.md).

## 🔒 Privacy & Security

This system is designed with **privacy-first principles**:

- ✅ **All audio processing happens locally** on your Mac
- ✅ **No audio files are ever uploaded** to external servers
- ✅ **LLM processing is local** using Ollama
- ✅ **Internet only used** for downloading models (one-time)
- ✅ **Full HIPAA compliance** when used properly

You can verify this by running: `python verify_privacy.py`

## 🎛️ Advanced Command Line Options

### Speaker Diarization Options

The system offers three levels of speaker identification:

```bash
# Simple diarization (default) - fast, based on speech pauses
python run.py audio.wav --diarization simple

# Advanced diarization - AI-powered with pyannote.audio (requires setup above)
python run.py audio.wav --diarization advanced

# Advanced + LLM post-processing - AI diarization + LLM speaker role enhancement
python run.py audio.wav --diarization advanced-with-llm-post-processing

# Auto mode - uses advanced if available, falls back to simple
python run.py audio.wav --diarization auto
```

**Diarization Method Details**:
- **Simple**: Fast pause-based speaker switching (no external dependencies)
- **Advanced**: Neural network speaker identification using pyannote.audio (most accurate)
- **Advanced + LLM**: pyannote.audio + AI analysis to improve therapist/client role assignment
- **Auto**: Uses advanced if pyannote.audio is available, otherwise falls back to simple

**Advanced Diarization Features**:
- More accurate speaker identification using neural networks
- Better handling of overlapping speech
- Improved separation of multiple speakers
- All processing remains local and private

**Requirements for Advanced Diarization**:
- Hugging Face token (free, see setup above)
- Additional ~500MB for AI models (downloaded once)
- Requires `pip install -r requirements-advanced.txt`

### Other Command Line Options

```bash
# Use different Whisper models (trade speed vs accuracy)
python run.py audio.wav --whisper-model tiny     # Fastest
python run.py audio.wav --whisper-model base     # Default
python run.py audio.wav --whisper-model medium   # Better accuracy
python run.py audio.wav --whisper-model large    # Best accuracy

# Specify output directory
python run.py audio.wav --output /path/to/results

# Use different LLM model
python run.py audio.wav --llm-model codellama

# Basic mode (disables advanced features)
python run.py audio.wav --basic-mode

# Disable LLM-enhanced speaker analysis
python run.py audio.wav --no-llm-enhancement

# Enable verbose logging
python run.py audio.wav --verbose
```

### Working with Real Audio Files

The system works with:
- ✅ WAV files (best)
- ✅ MP3 files
- ✅ M4A files
- ✅ Most common audio formats

For best results:
- Clear audio with minimal background noise
- Session length: 15 minutes to 2+ hours
- Two speakers (therapist and client)

## 📚 Next Steps

Once you have the basic system working:

1. **Explore Templates**: Check out the templates in `templates/` folder
2. **Customize Prompts**: Modify the LLM prompts in `app/core.py`
3. **Advanced Features**: Follow the [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md)
4. **Theme Modes**: Explore the personality modes in `app/modes/`

## 🆘 Need Help?

### Quick Fixes

**"Command not found" errors**:
- Restart Terminal completely
- Make sure you followed the PATH setup steps

**Python version issues**:
```bash
# Check ASDF is working
asdf current

# Reinstall the Python version if needed
asdf install python 3.12.11
```

**ffmpeg errors**:
```bash
# Reinstall ffmpeg
brew reinstall ffmpeg

# Check it's in your PATH
which ffmpeg
```

**Advanced diarization errors**:
```bash
# Check if advanced dependencies are installed
pip list | grep torch
pip list | grep pyannote

# Reinstall advanced dependencies if needed
pip install -r requirements-advanced.txt

# Verify privacy and test setup
python verify_privacy.py
```

### Comprehensive Help

- **Full troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **ffmpeg installation**: [docs/FFMPEG_INSTALL.md](docs/FFMPEG_INSTALL.md)
- **Development roadmap**: [docs/DEVELOPMENT_ROADMAP.md](docs/DEVELOPMENT_ROADMAP.md)

### Still Stuck?

1. Run `python test_installation.py` and share the output
2. Include your macOS version: `sw_vers`
3. Include your Python version: `python3 --version`
4. Include the exact error message

---

## 📚 Documentation Directory

### Essential Guides
| Document | Description | When to Use |
|----------|-------------|-------------|
| **[QUICK_START.md](QUICK_START.md)** | **👈 You are here!** Complete setup guide for new Mac users | Start here for first-time setup |
| **[README.md](README.md)** | Project overview and quick reference | Understanding the project goals |

### Troubleshooting & Installation
| Document | Description | When to Use |
|----------|-------------|-------------|
| **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** | Comprehensive problem-solving guide | When you encounter errors or issues |
| **[docs/FFMPEG_INSTALL.md](docs/FFMPEG_INSTALL.md)** | Manual ffmpeg installation instructions | When automated ffmpeg install fails |
| **[docs/INSTALL.md](docs/INSTALL.md)** | Legacy installation guide | Alternative installation methods |

### Development & Advanced Usage
| Document | Description | When to Use |
|----------|-------------|-------------|
| **[docs/ADVANCED_DIARIZATION_GUIDE.md](docs/ADVANCED_DIARIZATION_GUIDE.md)** | Advanced speaker diarization setup and privacy guide | Setting up AI-powered speaker identification |
| **[docs/CODE_WALKTHROUGH.md](docs/CODE_WALKTHROUGH.md)** | Technical architecture and code analysis | Understanding how the system works (SRE/Developer) |
| **[docs/DEVELOPMENT_ROADMAP.md](docs/DEVELOPMENT_ROADMAP.md)** | 5-phase development plan with learning resources | Planning future development |
| **[docs/PROJECT_IMPLEMENTATION_SUMMARY.md](docs/PROJECT_IMPLEMENTATION_SUMMARY.md)** | Implementation summary and design decisions | High-level technical overview |
| **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)** | Guidelines for contributing to the project | When you want to contribute code or improvements |

### Templates & Examples
| Directory | Description | When to Use |
|-----------|-------------|-------------|
| **[templates/](templates/)** | Clinical note templates (SOAP, BIRP, etc.) | Customizing output formats |
| **[example_data/](example_data/)** | Demo transcripts and test materials | Creating test audio files |
| **[app/modes/](app/modes/)** | Theme mode documentation | Exploring personality modes |

### Utility Scripts
| Script | Description | When to Use |
|--------|-------------|-------------|
| **[setup.sh](setup.sh)** | Automated installation script | Initial project setup |
| **[check_asdf.sh](check_asdf.sh)** | Verify ASDF and Python setup | Troubleshooting Python versions |
| **[test_installation.py](test_installation.py)** | Test all components work | Verifying successful installation |
| **[create_demo.py](create_demo.py)** | Generate example materials | Creating test data |
| **[verify_privacy.py](verify_privacy.py)** | Verify local-only processing and privacy | Confirming no data leaves your computer |

---

*🎉 Congratulations! You've set up a complete AI-powered therapy session processor that runs entirely on your Mac, protecting client privacy while providing professional-grade clinical documentation.*

## Common Issues

### "tkinter" or "Python version" Errors
- **Quick Fix**: Use `pip install -r requirements-legacy.txt` instead
- **Full Guide**: See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for detailed solutions

### "Ollama not running" Error
- Make sure Ollama is installed and running
- Check: `ollama list` to see available models
- Try: `ollama pull llama3.2` to download the default model

### Audio Processing Errors
- Ensure your audio file is in WAV, MP3, or M4A format
- Large files (>1 hour) may take significant time to process
- For best results, use clear audio with minimal background noise

### Memory Issues
- Use smaller Whisper models (`tiny` or `base`) for limited RAM
- Process shorter audio segments if needed
- Close other applications to free up memory

**For complete troubleshooting**: See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

## Performance Tips

1. **Audio Quality**: Clear, uncompressed audio works best
2. **Whisper Model**: Start with `base`, upgrade to `medium` or `large` for better accuracy
3. **LLM Model**: `llama3.2` is the default, `codellama` might work better for some tasks
4. **Hardware**: GPU acceleration helps but isn't required

## Next Steps

Once you have the basic system working:

1. Review the generated SOAP notes for accuracy
2. Customize templates in the `templates/` folder
3. Explore the theme modes in `app/modes/`
4. Consider the advanced features in the roadmap

## Getting Help

- Check the `DEVELOPMENT_ROADMAP.md` for planned features
- Review error messages carefully - they often contain helpful information
- Use the `--verbose` flag to see detailed processing information
- Join Python/AI communities for technical support

---

*Remember: This tool is designed to assist with clinical documentation, not replace professional judgment. Always review and edit the generated notes before using them in clinical practice.*

**Advanced diarization errors**:
```bash
# Check if advanced dependencies are installed
pip list | grep torch
pip list | grep pyannote

# Reinstall advanced dependencies if needed
pip install -r requirements-advanced.txt

# Verify privacy and test setup
python verify_privacy.py
```
