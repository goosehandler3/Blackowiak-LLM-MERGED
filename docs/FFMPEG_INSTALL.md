# MANUAL FFMPEG INSTALLATION GUIDE

If the automated setup script doesn't install ffmpeg successfully, you can install it manually:

## macOS

### Option 1: Homebrew (Recommended)
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install ffmpeg
brew install ffmpeg
```

### Option 2: MacPorts
```bash
sudo port install ffmpeg
```

### Option 3: Download Binary
1. Go to https://ffmpeg.org/download.html
2. Download the macOS build
3. Extract and add to your PATH

## Ubuntu/Debian Linux

```bash
sudo apt update
sudo apt install ffmpeg portaudio19-dev
```

## CentOS/RHEL/Fedora

```bash
# Fedora
sudo dnf install ffmpeg portaudio-devel

# CentOS/RHEL (enable EPEL first)
sudo yum install epel-release
sudo yum install ffmpeg portaudio-devel
```

## Windows

### Option 1: Chocolatey
```cmd
choco install ffmpeg
```

### Option 2: Manual Download
1. Go to https://ffmpeg.org/download.html#build-windows
2. Download a Windows build
3. Extract to a folder (e.g., C:\ffmpeg)
4. Add C:\ffmpeg\bin to your PATH environment variable

### Option 3: Windows Subsystem for Linux (WSL)
```bash
sudo apt update && sudo apt install ffmpeg
```

## Verification

After installation, verify ffmpeg is working:

```bash
ffmpeg -version
```

You should see version information. If you get "command not found", ffmpeg isn't in your PATH.

## Common Issues

### "Command not found" after installation
- **Solution**: Restart your terminal/command prompt
- **macOS**: You may need to restart Terminal entirely
- **Windows**: You may need to log out and back in

### PATH Issues
If ffmpeg is installed but not found:

**macOS/Linux**:
```bash
# Find where ffmpeg is installed
which ffmpeg
whereis ffmpeg

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="/usr/local/bin:$PATH"
```

**Windows**:
1. Search for "Environment Variables" in Start Menu
2. Click "Environment Variables"
3. Find "Path" in System Variables
4. Add the folder containing ffmpeg.exe

### Permission Issues (Linux)
```bash
# If you get permission errors
sudo chmod +x /usr/local/bin/ffmpeg
```

## Testing Audio Processing

Once ffmpeg is installed, test the Blackowiak LLM system:

```bash
# Activate virtual environment
source venv/bin/activate

# Test installation
python test_installation.py

# Process an audio file
python run.py your_audio_file.wav
```

## Alternative: Docker Installation

If you're having persistent issues, you can use Docker:

```bash
# Build with all dependencies
docker build -t blackowiak-llm .

# Run with audio file
docker run -v $(pwd):/workspace blackowiak-llm python run.py audio.wav
```

(Note: Docker setup would require creating a Dockerfile)

---

**Need more help?** Check the main [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide or file an issue on GitHub.
