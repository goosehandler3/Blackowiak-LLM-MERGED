# TROUBLESHOOTING GUIDE

## New Mac Setup Issues

### Issue 1: Xcode Command Line Tools Not Installed
```
xcode-select: error: command line tools not found
```

**Solution**: Install Xcode Command Line Tools first:
```bash
xcode-select --install
```
This opens a dialog - click "Install" and wait 10-30 minutes.

### Issue 2: Homebrew Not Found
```
brew: command not found
```

**Solution**: Install Homebrew:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Important: Follow the "Next steps" output to add Homebrew to PATH
# It will show commands like:
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Issue 3: ASDF Not Working
```
asdf: command not found
```

**Solution**: Install and configure ASDF:
```bash
# Install via Homebrew
brew install asdf

# Add to shell profile (for zsh - default on new Macs)
echo '. /opt/homebrew/opt/asdf/libexec/asdf.sh' >> ~/.zshrc

# Restart terminal or reload profile
source ~/.zshrc

# Verify installation
asdf --version
```

### Issue 4: Wrong Python Version
```
Python 3.x.x but need 3.12.11
```

**Solution**: Use ASDF to install the correct Python version:
```bash
# Add Python plugin if not already added
asdf plugin add python

# Install the required version
asdf install python 3.12.11

# Set as global default
asdf global python 3.12.11

# Verify
python3 --version  # Should show 3.12.11
```

**Quick Check**: Run the ASDF verification script:
```bash
./check_asdf.sh
```

## Common Installation Issues and Solutions

### Issue 1: tkinter Error
```
ERROR: No matching distribution found for tkinter>=8.6
```

**Solution**: tkinter is built into Python and doesn't need to be installed separately. This has been fixed in the updated requirements.txt.

### Issue 2: Python Version Compatibility
```
ERROR: Ignored the following versions that require a different python version
```

**Root Cause**: Some packages require Python 3.10+ but you have Python 3.8 or 3.9.

**Solutions**:
1. **Use the legacy requirements** (Recommended):
   ```bash
   pip install -r requirements-legacy.txt
   ```

2. **Upgrade Python** (Advanced):
   - Install Python 3.10+ from [python.org](https://python.org)
   - Or use pyenv: `pyenv install 3.11` then `pyenv local 3.11`

### Issue 3: Audio Processing Dependencies
```
ERROR: Failed building wheel for some-audio-package
```

**Solution**: Install system audio libraries first:

**macOS**:
```bash
brew install portaudio ffmpeg
pip install -r requirements.txt
```

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev ffmpeg libsndfile1
pip install -r requirements.txt
```

**Windows**:
```bash
# Install via conda (recommended for Windows)
conda install pytorch torchaudio -c pytorch
pip install -r requirements.txt
```

### Issue 4: PyTorch Installation Issues
```
ERROR: Could not find a version that satisfies the requirement torch
```

**Solution**: Install PyTorch separately first:
```bash
# For CPU-only (most common)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Then install other requirements
pip install -r requirements.txt
```

### Issue 5: Whisper Installation Issues
```
ERROR: Failed to build whisper
```

**Solution**: Install system dependencies:

**macOS**:
```bash
brew install rust
pip install --upgrade pip setuptools wheel
pip install openai-whisper
```

**Linux**:
```bash
sudo apt-get install build-essential
pip install --upgrade pip setuptools wheel
pip install openai-whisper
```

### Issue 6: Ollama Connection Issues
```
❌ Ollama is not running
```

**Solution**:
1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai/)
2. **Start Ollama**: It usually starts automatically, but you can run `ollama serve`
3. **Download a model**: `ollama pull llama3.2`
4. **Test**: `ollama list` should show your models

### Issue 7: Virtual Environment Issues
```
Command 'python' not found
```

**Solution**: Make sure you've activated the virtual environment:
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# You should see (venv) in your prompt
```

### Issue 8: Memory Issues During Processing
```
RuntimeError: CUDA out of memory
```

**Solution**: Use smaller models or CPU processing:
```bash
# Use smaller Whisper model
python run.py audio.wav --whisper-model tiny

# Force CPU usage (if you have GPU issues)
export CUDA_VISIBLE_DEVICES=""
python run.py audio.wav
```

## Step-by-Step Troubleshooting

### 1. Clean Installation
If you're having multiple issues, try a clean installation:

```bash
# Remove existing virtual environment
rm -rf venv

# Create new virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install system dependencies (if needed)
# macOS: brew install portaudio ffmpeg
# Linux: sudo apt-get install portaudio19-dev ffmpeg

# Try legacy requirements first
pip install -r requirements-legacy.txt
```

### 2. Test Individual Components
Test each part separately:

```bash
# Test Python version
python3 --version

# Test basic imports
python3 -c "import sys; print('Python OK')"

# Test audio processing
python3 -c "import librosa; print('Audio OK')"

# Test LLM connection
python3 -c "import requests; print('Network OK')"

# Test Whisper
python3 -c "import whisper; print('Whisper OK')"

# Run full installation test
python test_installation.py
```

### 3. Alternative Installation Methods

**Option A: Conda (Recommended for Windows)**
```bash
conda create -n blackowiak python=3.11
conda activate blackowiak
conda install pytorch torchaudio -c pytorch
pip install -r requirements.txt
```

**Option B: Docker (Advanced)**
```bash
# Build container
docker build -t blackowiak-llm .

# Run container
docker run -v $(pwd):/workspace blackowiak-llm
```

**Option C: Manual Installation**
```bash
# Install core dependencies one by one
pip install torch torchaudio
pip install openai-whisper
pip install requests rich click
pip install librosa soundfile pydub
pip install pandas numpy
pip install ollama
```

## Getting Help

### Before Asking for Help:
1. ✅ Run `python test_installation.py` and share the output
2. ✅ Share your Python version: `python3 --version`
3. ✅ Share your OS: macOS/Linux/Windows
4. ✅ Share the exact error message
5. ✅ Try the solutions above first

### Where to Get Help:
- **GitHub Issues**: File an issue in the repository
- **Python Community**: [r/learnpython](https://reddit.com/r/learnpython)
- **AI/ML Community**: [Hugging Face Forums](https://discuss.huggingface.co/)
- **Audio Processing**: [librosa GitHub](https://github.com/librosa/librosa)

## Success Indicators

You'll know everything is working when:
- ✅ `python test_installation.py` passes all tests
- ✅ `python run.py --help` shows the help message
- ✅ You can process a small audio file without errors
- ✅ Ollama responds to `ollama list`

## Performance Optimization

Once everything is working:
- **Faster Processing**: Use `--whisper-model tiny` for speed
- **Better Accuracy**: Use `--whisper-model medium` or `large`
- **Less Memory**: Close other applications during processing
- **GPU Acceleration**: Install CUDA-enabled PyTorch if you have an NVIDIA GPU

---

*Remember: The goal is to get a working system first, then optimize. Don't try to solve all issues at once - tackle them one by one.*
