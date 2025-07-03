#!/bin/bash

# ASDF and Python Version Check Script
# This script verifies that ASDF and Python are properly configured

echo "🔍 Checking ASDF and Python Setup"
echo "=================================="

# Check if ASDF is installed
if ! command -v asdf &> /dev/null; then
    echo "❌ ASDF is not installed or not in PATH"
    echo ""
    echo "To install ASDF:"
    echo "1. brew install asdf"
    echo "2. Add to your shell profile:"
    echo "   echo '. /opt/homebrew/opt/asdf/libexec/asdf.sh' >> ~/.zshrc"
    echo "3. Restart terminal or run: source ~/.zshrc"
    exit 1
else
    echo "✅ ASDF is installed: $(asdf --version)"
fi

# Check if Python plugin is installed
if ! asdf plugin list | grep -q python; then
    echo "❌ Python plugin for ASDF is not installed"
    echo ""
    echo "To install Python plugin:"
    echo "asdf plugin add python"
    exit 1
else
    echo "✅ Python plugin is installed"
fi

# Check if the required Python version is installed
REQUIRED_VERSION="3.12.11"
if ! asdf list python | grep -q "$REQUIRED_VERSION"; then
    echo "❌ Python $REQUIRED_VERSION is not installed"
    echo ""
    echo "To install the required Python version:"
    echo "asdf install python $REQUIRED_VERSION"
    echo "asdf global python $REQUIRED_VERSION"
    exit 1
else
    echo "✅ Python $REQUIRED_VERSION is installed"
fi

# Check current Python version
CURRENT_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
if [[ "$CURRENT_VERSION" == "$REQUIRED_VERSION" ]]; then
    echo "✅ Python $CURRENT_VERSION is currently active (matches required $REQUIRED_VERSION)"
else
    echo "⚠️  Python $CURRENT_VERSION is active, but $REQUIRED_VERSION is required"
    echo ""
    echo "To set the correct version:"
    echo "asdf global python $REQUIRED_VERSION"
    echo "# Then restart your terminal"
fi

# Check if .tool-versions file exists and matches
if [[ -f ".tool-versions" ]]; then
    TOOL_VERSION=$(grep python .tool-versions | cut -d' ' -f2)
    if [[ "$TOOL_VERSION" == "$REQUIRED_VERSION" ]]; then
        echo "✅ .tool-versions file matches required Python version"
    else
        echo "⚠️  .tool-versions specifies Python $TOOL_VERSION, but we're checking for $REQUIRED_VERSION"
    fi
else
    echo "❌ .tool-versions file not found in current directory"
    echo "   Make sure you're in the blackowiak-llm project directory"
fi

# Check if pip is working
if python3 -m pip --version &> /dev/null; then
    echo "✅ pip is working with the current Python"
else
    echo "❌ pip is not working with the current Python"
fi

# Summary
echo ""
echo "🎯 Summary:"
echo "- ASDF: $(asdf --version)"
echo "- Python: $(python3 --version)"
echo "- pip: $(python3 -m pip --version | cut -d' ' -f1-2)"

if [[ "$CURRENT_VERSION" == "$REQUIRED_VERSION" ]]; then
    echo ""
    echo "🎉 Everything looks good! You can proceed with the setup."
    echo "Next step: ./setup.sh"
else
    echo ""
    echo "🔧 Please fix the Python version before continuing."
fi
