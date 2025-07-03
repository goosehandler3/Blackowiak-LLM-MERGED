#!/bin/bash
"""
Blackowiak LLM - Build Script for Commercial Distribution

This script packages the application into a standalone executable.
"""

set -e

echo "🔨 Building Blackowiak LLM Commercial Package"
echo "============================================="

# Check if we're in the right directory
if [ ! -f "run.py" ]; then
    echo "❌ Error: Must run from the project root directory"
    exit 1
fi

# Create build directory
mkdir -p dist/
rm -rf dist/blackowiak-llm-*

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install pyinstaller

# Create the executable
echo "🔧 Creating standalone executable..."

# Option 1: Single file (larger, slower startup)
pyinstaller \
    --onefile \
    --name blackowiak-llm \
    --add-data "templates:templates" \
    --add-data "requirements.txt:." \
    --add-data "license_manager.py:." \
    --hidden-import pyannote.audio \
    --hidden-import torch \
    --hidden-import whisper \
    --hidden-import pydub \
    --hidden-import rich \
    --hidden-import requests \
    --collect-all torch \
    --collect-all whisper \
    --noconfirm \
    run.py

# Option 2: Directory distribution (smaller, faster startup)
pyinstaller \
    --name blackowiak-llm-dir \
    --add-data "templates:templates" \
    --add-data "requirements.txt:." \
    --add-data "license_manager.py:." \
    --hidden-import pyannote.audio \
    --hidden-import torch \
    --hidden-import whisper \
    --hidden-import pydub \
    --hidden-import rich \
    --hidden-import requests \
    --collect-all torch \
    --collect-all whisper \
    --noconfirm \
    run.py

# Create distribution package
echo "📋 Creating distribution package..."

# Create README for customers
cat > dist/README.txt << 'EOF'
BLACKOWIAK LLM - THERAPY SESSION PROCESSOR
==========================================

Thank you for purchasing Blackowiak LLM!

SYSTEM REQUIREMENTS:
- macOS 10.15+ (Catalina or newer)
- 4GB+ RAM available
- 2GB free disk space
- Internet connection for initial setup only

INSTALLATION:
1. Extract this package to your Applications folder
2. Activate your license (see below)
3. Install Ollama: https://ollama.ai/
4. Run: ollama pull llama3.2

ACTIVATION:
Open Terminal and run:
  ./blackowiak-llm --activate-license YOUR_LICENSE_CODE

USAGE:
Basic usage:
  ./blackowiak-llm audio_file.wav

Advanced usage:
  ./blackowiak-llm audio_file.wav --diarization advanced --output results/

For full help:
  ./blackowiak-llm --help

SUPPORT:
Email: support@blackowiak-llm.com
Website: https://blackowiak-llm.com/support

PRIVACY:
All audio processing happens locally on your computer.
No audio data is ever uploaded to external servers.
EOF

# Create license generator for you
cat > dist/generate_license.py << 'EOF'
#!/usr/bin/env python3
"""
License Generator for Blackowiak LLM
Use this to generate license codes for customers.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from license_manager import generate_license_cli

if __name__ == "__main__":
    generate_license_cli()
EOF

chmod +x dist/generate_license.py

# Copy license manager
cp license_manager.py dist/

# Create final package structure
mkdir -p "dist/Blackowiak-LLM-Commercial"
cp dist/blackowiak-llm "dist/Blackowiak-LLM-Commercial/"
cp -r dist/blackowiak-llm-dir "dist/Blackowiak-LLM-Commercial/"
cp dist/README.txt "dist/Blackowiak-LLM-Commercial/"
cp -r templates "dist/Blackowiak-LLM-Commercial/"
cp -r example_data "dist/Blackowiak-LLM-Commercial/"

# Create vendor package (for you)
mkdir -p "dist/Vendor-Tools"
cp dist/generate_license.py "dist/Vendor-Tools/"
cp dist/license_manager.py "dist/Vendor-Tools/"

cat > dist/Vendor-Tools/README.txt << 'EOF'
VENDOR TOOLS - BLACKOWIAK LLM
=============================

Use these tools to manage licenses for your customers.

GENERATE LICENSE:
  python generate_license.py --email customer@example.com --type standard --days 365

LICENSE TYPES:
- trial: 30 days, 10 uses
- standard: 365 days, unlimited uses  
- professional: 365 days, unlimited uses + advanced features

EXAMPLES:
  # 30-day trial
  python generate_license.py --email test@example.com --type trial --days 30 --max-uses 10
  
  # 1-year standard license
  python generate_license.py --email customer@example.com --type standard
  
  # 6-month professional license
  python generate_license.py --email pro@example.com --type professional --days 180
EOF

echo "✅ Build completed!"
echo ""
echo "📁 Distribution files created:"
echo "   dist/Blackowiak-LLM-Commercial/  <- Customer package"
echo "   dist/Vendor-Tools/               <- Your license management tools"
echo ""
echo "🚀 Next steps:"
echo "   1. Test the executable: dist/Blackowiak-LLM-Commercial/blackowiak-llm --help"
echo "   2. Generate test license: cd dist/Vendor-Tools && python generate_license.py --email test@example.com --type trial --days 30"
echo "   3. Create installer/DMG for distribution"
echo ""
echo "💰 Ready for commercial distribution!"
