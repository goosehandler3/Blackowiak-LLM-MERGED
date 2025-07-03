#!/bin/bash
#
# Blackowiak LLM - macOS Commercial Build Script
# ==============================================
#
# This is a macOS-only build system for commercial distribution.
# Windows and Linux builds are disabled and commented out.
#
# For multi-platform builds:
# - Use Windows machines for Windows builds with cx_Freeze
# - Use Linux machines for Linux builds with PyInstaller
# - This script handles macOS binaries and DMG creation only
#
# Features:
# - macOS binary compilation with PyInstaller
# - DMG installer creation
# - Customer package preparation
# - Vendor tool generation
# - License management integration
#

set -e

echo "🏗️ Blackowiak LLM - macOS Commercial Builder"
echo "=============================================="

# Parse command line arguments
BUILD_TYPE="${1:-all}"  # all, binary, dmg, vendor, cache-info, clean-cache (macOS-only build system)
VERSION="${2:-1.0.0}"

echo "📋 Build Configuration (macOS Only):"
echo "   Build Type: $BUILD_TYPE"
echo "   Version: $VERSION"
echo "   Platform: macOS (Commercial Edition)"
echo "   Cache: Enabled for faster rebuilds"
echo ""

# Create build environment with cache support
echo "🧹 Preparing build environment..."
BUILD_CACHE_DIR="$HOME/.blackowiak-llm-build-cache"
mkdir -p "$BUILD_CACHE_DIR"/{pip,pyinstaller,workpath}

# Clean dist and build dirs but pres/Users/jeremy.blackowiak/Applications/Blackowiak-LLMerve cache
rm -rf dist/ build/ *.spec
mkdir -p dist/

echo "📂 Using build cache directory: $BUILD_CACHE_DIR"

# Install build dependencies for macOS with cache
echo "📦 Installing macOS build dependencies..."
python -m pip install --cache-dir "$BUILD_CACHE_DIR/pip" pyinstaller dmgbuild

# Verify PyInstaller is available
if ! command -v pyinstaller &> /dev/null; then
    echo "⚠️ PyInstaller not found in PATH, trying python -m PyInstaller..."
    PYINSTALLER_CMD="python -m PyInstaller"
else
    PYINSTALLER_CMD="pyinstaller"
fi

echo "💾 Cache locations:"
echo "   Pip cache: $BUILD_CACHE_DIR/pip"
echo "   PyInstaller cache: $BUILD_CACHE_DIR/pyinstaller"
echo "   Work files: $BUILD_CACHE_DIR/workpath"

# Create version info
cat > version_info.py << EOF
__version__ = "$VERSION"
__build_date__ = "$(date -u +%Y-%m-%d)"
__author__ = "Andrew Blackowiak"
__license__ = "Commercial"
EOF

# Function to build macOS binary
build_macos_binary() {
    echo "🍎 Building macOS binary..."
    
    # Check if we have a cached binary that's newer than source files
    CACHE_BINARY="$BUILD_CACHE_DIR/pyinstaller/blackowiak-llm-$VERSION"
    if [ -f "$CACHE_BINARY" ] && [ "$CACHE_BINARY" -nt "run.py" ] && [ "$CACHE_BINARY" -nt "license_manager.py" ] && [ "$CACHE_BINARY" -nt "app/core.py" ]; then
        echo "🚀 Found cached binary, copying to dist..."
        cp "$CACHE_BINARY" "dist/blackowiak-llm-$VERSION"
        echo "✅ macOS binary restored from cache: dist/blackowiak-llm-$VERSION"
        return
    fi
    
    echo "🔨 Building new binary (cache miss or source files changed)..."
    
    # Note: We do NOT pre-download Hugging Face models during build because:
    # 1. Many models require authentication tokens
    # 2. Models are large and would bloat the binary significantly
    # 3. Users must authenticate with Hugging Face themselves for model access
    # 4. Models are cached locally after first download, so only first use requires internet
    
    echo "📋 Build notes:"
    echo "   • Hugging Face models will be downloaded on first use"
    echo "   • Users must authenticate with Hugging Face if required"
    echo "   • Internet connection required for initial model setup"
    echo "   • All processing happens locally after initial setup"
    
    # No Hugging Face cache bundling - let users handle authentication
    HF_CACHE_ARG=""
    
    # Create excludes file to avoid bundling unnecessary modules
    cat > excludes.txt << 'EOF'
# Windows-specific modules (we're on macOS)
_winapi
msvcrt
nt
winreg
_overlapped

# Development and testing modules
pytest
unittest
doctest
pdb
cProfile
profile

# Jupyter/IPython (not needed for CLI)
IPython
jupyter
notebook

# Matplotlib backends (reduce bloat)
matplotlib.backends._backend_pdf
matplotlib.backends._backend_ps
matplotlib.backends._backend_svg
matplotlib.backends.backend_qt5agg
matplotlib.backends.backend_tkagg

# Unused ML frameworks
tensorflow
keras
jax
flax

# Documentation generators
sphinx
mkdocs

# Linters and formatters (not needed at runtime)
pylint
flake8
black
autopep8

# Version control
git
hg
bzr
EOF

    $PYINSTALLER_CMD \
        --name "blackowiak-llm-$VERSION" \
        --onefile \
        --console \
        --workpath "$BUILD_CACHE_DIR/workpath" \
        --distpath "dist" \
        --add-data "templates:templates" \
        --add-data "example_data:example_data" \
        --add-data "app:app" \
        --add-data "license_manager.py:." \
        --add-data "version_info.py:." \
        --add-data "requirements.txt:." \
        $HF_CACHE_ARG \
        --hidden-import app.core \
        --hidden-import torch \
        --hidden-import whisper \
        --hidden-import pydub \
        --hidden-import rich \
        --hidden-import requests \
        --hidden-import librosa \
        --hidden-import soundfile \
        --hidden-import click \
        --hidden-import cryptography \
        --hidden-import psutil \
        --hidden-import platform \
        --hidden-import numpy \
        --hidden-import scipy \
        --hidden-import pyannote.audio \
        --hidden-import pyannote.core \
        --hidden-import pyannote.pipeline \
        --hidden-import pyannote.database \
        --hidden-import huggingface_hub \
        --collect-all torch \
        --collect-all whisper \
        --collect-all pyannote \
        --copy-metadata torch \
        --copy-metadata torchaudio \
        --copy-metadata openai-whisper \
        --copy-metadata huggingface-hub \
        --exclude-module _winapi \
        --exclude-module msvcrt \
        --exclude-module nt \
        --exclude-module winreg \
        --exclude-module _overlapped \
        --exclude-module lightning_fabric \
        --exclude-module pytorch_lightning \
        --exclude-module tensorflow \
        --exclude-module keras \
        --exclude-module matplotlib.backends._backend_pdf \
        --exclude-module matplotlib.backends._backend_ps \
        --exclude-module matplotlib.backends._backend_svg \
        --exclude-module matplotlib.backends.backend_qt5agg \
        --exclude-module matplotlib.backends.backend_tkagg \
        --exclude-module IPython \
        --exclude-module jupyter \
        --exclude-module notebook \
        --noconfirm \
        run.py
    
    # Cache the built binary for next time
    if [ -f "dist/blackowiak-llm-$VERSION" ]; then
        cp "dist/blackowiak-llm-$VERSION" "$CACHE_BINARY"
        echo "💾 Binary cached for future builds"
    fi
    
    echo "✅ macOS binary created: dist/blackowiak-llm-$VERSION"
}

# Function to build macOS DMG
build_macos_dmg() {
    echo "📀 Building macOS DMG installer..."
    
    # First build the binary if not exists
    if [ ! -f "dist/blackowiak-llm-$VERSION" ]; then
        build_macos_binary
    fi
    
    # Create DMG structure
    mkdir -p "dist/dmg/Blackowiak LLM"
    cp "dist/blackowiak-llm-$VERSION" "dist/dmg/Blackowiak LLM/"
    cp "dist/blackowiak-llm-$VERSION" "dist/dmg/Blackowiak LLM/blackowiak-llm"
    cp -r templates "dist/dmg/Blackowiak LLM/"
    cp -r example_data "dist/dmg/Blackowiak LLM/"
    cp installer.py "dist/dmg/Blackowiak LLM/"
    
    # Create README for DMG
    cat > "dist/dmg/Blackowiak LLM/READ ME FIRST.txt" << 'EOF'
BLACKOWIAK LLM - THERAPY SESSION PROCESSOR
==========================================

SYSTEM REQUIREMENTS:
- macOS 10.15+ (Catalina or newer)
- 4GB+ RAM available
- Internet connection for initial setup only
- 2GB+ free disk space for AI models

INSTALLATION:
1. Copy "Blackowiak LLM" folder to your Applications
2. Open Terminal and run the installer:
   python /Applications/Blackowiak\ LLM/installer.py

FIRST-TIME SETUP (Required):

1. INSTALL DEPENDENCIES:
   • Install Ollama: https://ollama.ai/
   • Install FFmpeg: brew install ffmpeg

2. DOWNLOAD AI MODELS:
   • Run: ollama pull llama3.2
   • This downloads the AI model for session summaries

3. ACTIVATE LICENSE:
   • Run: ./blackowiak-llm --activate-license YOUR_CODE
   • Your license code is provided with purchase

4. SETUP ADVANCED FEATURES (Optional):
   • Create free Hugging Face account: https://huggingface.co/join
   • Get access token: https://huggingface.co/settings/tokens
   • Accept model license: https://huggingface.co/pyannote/speaker-diarization-3.1
   • Login: huggingface-cli login
   • This enables advanced speaker identification

WHAT WORKS WITHOUT SETUP:
- Basic audio transcription
- Basic speaker detection
- All processing happens locally on your Mac

WHAT REQUIRES SETUP:
- AI-powered session summaries (needs Ollama)
- Advanced speaker diarization (needs Hugging Face)
- Various audio formats (needs FFmpeg)

DAILY USAGE:
./blackowiak-llm your_audio_file.wav

PRIVACY & SECURITY:
- All processing happens on your computer
- No data sent to external servers
- Internet only needed for initial model downloads
- Models cache locally for offline use

SUPPORT:
Email: support@blackowiak-llm.com
Website: https://blackowiak-llm.com
EOF
    
    # Create DMG settings
    cat > dmg_settings.py << EOF
import os

# DMG settings
settings = {
    'filename': 'dist/Blackowiak-LLM-v$VERSION.dmg',
    'volume_name': 'Blackowiak LLM v$VERSION',
    'format': 'UDBZ',
    'size': '500M',
    'files': ['dist/dmg/Blackowiak LLM'],
    'badge_icon': None,
    'icon_locations': {
        'Blackowiak LLM': (100, 100),
    },
    'background': None,
    'show_status_bar': False,
    'show_tab_view': False,
    'show_toolbar': False,
    'show_pathbar': False,
    'show_sidebar': False,
    'sidebar_width': 180,
    'window_rect': ((100, 100), (640, 480)),
    'default_view': 'icon-view',
    'icon_size': 128,
}
EOF
    
    # Build DMG (macOS only)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        dmgbuild -s dmg_settings.py "Blackowiak LLM v$VERSION" "dist/Blackowiak-LLM-v$VERSION.dmg"
        echo "✅ DMG created: dist/Blackowiak-LLM-v$VERSION.dmg"
    else
        echo "⚠️ DMG creation requires macOS"
    fi
    
    # Cleanup
    rm -rf dist/dmg dmg_settings.py
}

# Cache management functions
clean_cache() {
    echo "🧹 Cleaning build cache..."
    rm -rf "$BUILD_CACHE_DIR"
    echo "✅ Cache cleaned"
}

show_cache_info() {
    echo "📊 Build Cache Information:"
    echo "   Location: $BUILD_CACHE_DIR"
    if [ -d "$BUILD_CACHE_DIR" ]; then
        echo "   Size: $(du -sh "$BUILD_CACHE_DIR" 2>/dev/null | cut -f1 || echo "Unknown")"
        echo "   Pip cache: $(find "$BUILD_CACHE_DIR/pip" -type f 2>/dev/null | wc -l) files"
        echo "   PyInstaller cache: $(find "$BUILD_CACHE_DIR/pyinstaller" -type f 2>/dev/null | wc -l) files"
        if [ -f "$BUILD_CACHE_DIR/pyinstaller/blackowiak-llm-$VERSION" ]; then
            echo "   Cached binary: ✅ Available ($(date -r "$BUILD_CACHE_DIR/pyinstaller/blackowiak-llm-$VERSION" 2>/dev/null || echo "unknown date"))"
        else
            echo "   Cached binary: ❌ Not available"
        fi
    else
        echo "   Status: Not initialized"
    fi
}

# Function to create vendor tools
create_vendor_tools() {
    echo "🔧 Creating vendor tools..."
    
    mkdir -p "dist/vendor-tools"
    
    # Copy license manager
    cp license_manager.py "dist/vendor-tools/"
    
    # Create license generation web interface
    cat > "dist/vendor-tools/web_license_generator.py" << 'EOF'
#!/usr/bin/env python3
"""
Web-based license generator for Blackowiak LLM
Simple Flask app for generating licenses
"""

from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from license_manager import LicenseManager

app = Flask(__name__)
license_manager = LicenseManager()

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Blackowiak LLM - License Generator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .form-group { margin: 15px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .result { background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin: 15px 0; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>🧠 Blackowiak LLM - License Generator</h1>
    
    <form id="licenseForm">
        <div class="form-group">
            <label for="email">Customer Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        
        <div class="form-group">
            <label for="type">License Type:</label>
            <select id="type" name="type">
                <option value="trial">Trial (30 days, 10 uses)</option>
                <option value="standard" selected>Standard (1 year, unlimited)</option>
                <option value="professional">Professional (1 year, unlimited + support)</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="days">Duration (days):</label>
            <input type="number" id="days" name="days" value="365">
        </div>
        
        <div class="form-group">
            <label for="max_uses">Max Uses (optional):</label>
            <input type="number" id="max_uses" name="max_uses" placeholder="Leave empty for unlimited">
        </div>
        
        <button type="submit">Generate License</button>
    </form>
    
    <div id="result" class="result" style="display: none;">
        <h3>License Generated</h3>
        <p><strong>Customer:</strong> <span id="result-email"></span></p>
        <p><strong>Type:</strong> <span id="result-type"></span></p>
        <p><strong>Duration:</strong> <span id="result-days"></span> days</p>
        <p><strong>License Code:</strong></p>
        <textarea id="license-code" style="width: 100%; height: 100px; font-family: monospace;"></textarea>
        <p><strong>Customer Activation Command:</strong></p>
        <code>python run.py --activate-license [LICENSE_CODE]</code>
    </div>
    
    <script>
        document.getElementById('licenseForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            fetch('/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    document.getElementById('result-email').textContent = data.email;
                    document.getElementById('result-type').textContent = data.type;
                    document.getElementById('result-days').textContent = data.days;
                    document.getElementById('license-code').value = result.license_code;
                    document.getElementById('result').style.display = 'block';
                } else {
                    alert('Error: ' + result.error);
                }
            });
        });
    </script>
</body>
</html>
    '''

@app.route('/generate', methods=['POST'])
def generate_license():
    try:
        data = request.json
        
        license_code = license_manager.generate_license_code(
            customer_email=data['email'],
            license_type=data['type'],
            duration_days=int(data['days']),
            max_uses=int(data['max_uses']) if data.get('max_uses') else None
        )
        
        return jsonify({
            'success': True,
            'license_code': license_code
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("🌐 Starting license generator web interface...")
    print("   Open: http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000)
EOF
    
    # Create requirements for web interface
    cat > "dist/vendor-tools/requirements-web.txt" << 'EOF'
flask>=2.0.0
EOF
    
    # Create vendor README
    cat > "dist/vendor-tools/README.md" << 'EOF'
# Blackowiak LLM - Vendor Tools

## License Generation

### Command Line
```bash
python license_manager.py --email customer@example.com --type standard --days 365
```

### Web Interface
```bash
pip install -r requirements-web.txt
python web_license_generator.py
# Open http://localhost:5000
```

## License Types

- **trial**: 30 days, 10 uses maximum
- **standard**: 365 days, unlimited uses
- **professional**: 365 days, unlimited uses + priority support

## Usage Examples

```bash
# Generate trial license
python license_manager.py --email trial@example.com --type trial --days 30 --max-uses 10

# Generate standard license
python license_manager.py --email customer@example.com --type standard

# Generate 6-month professional license
python license_manager.py --email pro@example.com --type professional --days 180
```
EOF
    
    echo "✅ Vendor tools created in dist/vendor-tools/"
}

# Function to create customer distribution packages
create_customer_packages() {
    echo "📦 Creating customer distribution packages..."
    
    # Create customer package directory
    mkdir -p "dist/customer-packages"
    
    # macOS Customer Package
    if [ -f "dist/blackowiak-llm-$VERSION" ]; then
        echo "📱 Creating macOS customer package..."
        
        mkdir -p "dist/customer-packages/Blackowiak-LLM-macOS"
        
        # Copy binary with both versioned and standard names
        cp "dist/blackowiak-llm-$VERSION" "dist/customer-packages/Blackowiak-LLM-macOS/"
        cp "dist/blackowiak-llm-$VERSION" "dist/customer-packages/Blackowiak-LLM-macOS/blackowiak-llm"
        
        # Copy installer and README only (minimal commercial package)
        cp installer.py "dist/customer-packages/Blackowiak-LLM-macOS/"
        cp CUSTOMER_README.md "dist/customer-packages/Blackowiak-LLM-macOS/README.md" 2>/dev/null || echo "⚠️ CUSTOMER_README.md not found"
        
        # Update customer README to only mention the binary and blackowiak command
        cat > "dist/customer-packages/Blackowiak-LLM-macOS/README.md" << 'EOF'
# Blackowiak LLM - Professional Edition

## Quick Installation

1. **Run the installer:**
   ```bash
   python installer.py
   ```

2. **Restart your terminal or run:**
   ```bash
   source ~/.zshrc
   ```

3. **Activate your license (placeholder):**
   ```bash
   blackowiak --activate-license YOUR_LICENSE_CODE
   ```

## Usage

Once installed, use the `blackowiak` command for all operations:

```bash
# Basic audio processing
blackowiak audio.wav

# With advanced diarization
blackowiak audio.wav --diarization advanced --hf-token YOUR_TOKEN

# Different LLM providers
blackowiak audio.wav --llm-provider openai --api-key YOUR_KEY
blackowiak audio.wav --llm-provider claude --api-key YOUR_KEY

# Output formats
blackowiak audio.wav --output-format SOAP
blackowiak audio.wav --output-format BIRP
blackowiak audio.wav --output-format DAP

# Help and options
blackowiak --help
blackowiak --version
```

## Dependencies

### Required Dependencies

**Ollama** (for local LLM processing):
- macOS: Download from https://ollama.ai/
- After installation: `ollama pull llama3.2`

**FFmpeg** (for audio processing):
- macOS: `brew install ffmpeg`

### Optional Dependencies

**Hugging Face** (for advanced diarization):
- Create account at https://huggingface.co/
- Generate token with "Inference API" access
- Accept pyannote/speaker-diarization-3.1 model license

**OpenAI** (for GPT models):
- Create account at https://platform.openai.com/
- Generate API key with billing enabled

**Anthropic** (for Claude models):  
- Create account at https://console.anthropic.com/
- Generate API key with billing enabled

## Features

- **Advanced Speaker Diarization**: Identify who spoke when using pyannote.audio
- **Multiple LLM Providers**: OpenAI GPT, Anthropic Claude, and local Ollama models
- **Professional Templates**: SOAP, BIRP, DAP, GIRP, and custom formats
- **Audio Processing**: Support for most audio formats via FFmpeg
- **Commercial License**: Professional-grade licensing and support

## Troubleshooting

**Command not found: blackowiak**
- Restart your terminal or run: `source ~/.zshrc`
- Check if `~/.local/bin` is in your PATH

**License activation failed**
- Verify your license code is correct
- Check internet connection
- Contact support if issues persist

**Audio processing errors**
- Ensure FFmpeg is installed: `ffmpeg -version`
- Check audio file format is supported
- Verify Ollama is running: `ollama list`

**Diarization errors**
- Ensure you have a valid Hugging Face token
- Verify you've accepted the pyannote model license
- Check internet connection for model downloads

## Support

- **Email**: support@blackowiak-llm.com
- **Website**: https://blackowiak-llm.com/support
- **License Issues**: https://blackowiak-llm.com/license-help

---

*Thank you for choosing Blackowiak LLM Professional Edition!*
EOF
        
        # Remove the START_HERE.txt creation since we have a focused README
        echo "✓ Customer package includes only binary and README"
    fi
    
    # NOTE: Windows and Linux packages are disabled in this macOS-only build
    # For multi-platform support, use platform-specific build machines
    
    echo "✅ macOS customer package created in dist/customer-packages/"
}

# Main build execution (macOS Only)
case $BUILD_TYPE in
    "binary"|"macos")
        build_macos_binary
        ;;
    "dmg")
        build_macos_dmg
        ;;
    "windows")
        echo "⚠️ Windows builds are disabled in this macOS-only version"
        echo "   Use a Windows machine for Windows builds"
        ;;
    "linux")
        echo "⚠️ Linux builds are disabled in this macOS-only version"
        echo "   Use a Linux machine for Linux builds"
        ;;
    "vendor")
        create_vendor_tools
        ;;
    "cache-info")
        show_cache_info
        exit 0
        ;;
    "clean-cache")
        clean_cache
        exit 0
        ;;
    "all"|*)
        echo "🚀 Building complete macOS commercial package..."
        build_macos_binary
        build_macos_dmg 2>/dev/null || echo "⚠️ DMG creation skipped (requires macOS)"
        create_vendor_tools
        create_customer_packages
        ;;
esac

# Cleanup
rm -f version_info.py *.spec

echo ""
echo "✅ macOS BUILD COMPLETE!"
echo "========================"
echo "📁 Distribution files:"
ls -la dist/
echo ""
show_cache_info
echo ""
echo "🚀 Next steps:"
echo "   1. Test the macOS binary on target machines"
echo "   2. Generate test licenses with vendor tools"
echo "   3. Create distribution packages (DMG, zip, etc.)"
echo "   4. Set up payment processing and website"
echo ""
echo "💰 Ready for macOS commercial launch!"
echo ""
echo "📝 Note: This is a macOS-only build system."
echo "   For Windows/Linux builds, use platform-specific machines."
echo ""
echo "🔧 Cache Commands:"
echo "   ./build_advanced.sh cache-info     - Show cache information"
echo "   ./build_advanced.sh clean-cache    - Clean build cache"
