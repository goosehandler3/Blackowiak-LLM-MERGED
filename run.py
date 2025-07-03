#!/usr/bin/env python3
"""
Blackowiak LLM - Main Entry Point

This is the main launcher for the Blackowiak LLM therapy session processor.
It provides a simple interface to the core audio processing functionality.
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

try:
    from core import main
    
    if __name__ == "__main__":
        print("🧠 Blackowiak LLM - Therapy Session Processor")
        print("=" * 50)
        print("Created by Andrew Blackowiak, MSW")
        print("Athens, GA · Therapist · Technologist · Millennial Futurist")
        print()
        
        # Run the main application
        exit_code = main()
        sys.exit(exit_code)
        
except ImportError as e:
    print("❌ Error: Missing dependencies!")
    print()
    print("Please install the required packages:")
    print("pip install -r requirements.txt")
    print()
    print("For local LLM support, also install Ollama:")
    print("https://ollama.ai/")
    print()
    print(f"Technical details: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)