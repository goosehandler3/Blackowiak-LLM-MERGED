#!/bin/bash

# Blackowiak LLM Setup Script
# This script sets up the development environment for the Blackowiak LLM project

echo "🧠 Setting up Blackowiak LLM Development Environment"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip3 found"

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Check for system dependencies
echo "🔍 Checking system dependencies..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg not found. Installing system dependencies..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "📦 Installing ffmpeg via Homebrew..."
            brew install ffmpeg
        else
            echo "❌ Homebrew not found. Please install ffmpeg manually:"
            echo "   1. Install Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            echo "   2. Run: brew install ffmpeg"
            echo "   3. Re-run this setup script"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "📦 Installing ffmpeg for Linux..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y ffmpeg portaudio19-dev
        elif command -v yum &> /dev/null; then
            sudo yum install -y ffmpeg portaudio-devel
        else
            echo "❌ Please install ffmpeg manually for your Linux distribution"
            exit 1
        fi
    else
        echo "❌ Unsupported OS. Please install ffmpeg manually"
        exit 1
    fi
else
    echo "✅ ffmpeg found"
fi

# Install core requirements
echo "📦 Installing core Python packages..."
if pip install -r requirements.txt; then
    echo "✅ Core packages installed successfully!"
else
    echo "⚠️  Some packages failed to install. Trying with legacy versions..."
    if pip install -r requirements-legacy.txt; then
        echo "✅ Legacy packages installed successfully!"
    else
        echo "❌ Package installation failed. Please check the error messages above."
        echo "   Common fixes:"
        echo "   - macOS: brew install portaudio ffmpeg"
        echo "   - Ubuntu: sudo apt-get install portaudio19-dev ffmpeg"
        exit 1
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Install Ollama: https://ollama.ai/"
echo "2. Run: ollama pull llama3.2"
echo "3. Activate the virtual environment: source venv/bin/activate"
echo "4. Test the installation: python test_installation.py"
echo ""
echo "To process an audio file:"
echo "python run.py path/to/your/audio.wav"
echo ""
