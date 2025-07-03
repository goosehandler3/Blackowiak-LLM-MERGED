#!/usr/bin/env python3
"""
Blackowiak LLM - Lightweight CLI Entry Point

This module provides a fast startup CLI that only imports heavy libraries when needed.
"""

import argparse
import sys
from pathlib import Path

def create_parser():
    """Create the argument parser without importing heavy libraries"""
    parser = argparse.ArgumentParser(
        description="Blackowiak LLM - Advanced Therapy Session Processor"
    )
    parser.add_argument(
        "audio_file", 
        nargs='?',  # Make audio_file optional for license commands
        help="Path to the audio file to process"
    )
    parser.add_argument(
        "-o", "--output", 
        default="output",
        help="Output directory for results (default: output)"
    )
    parser.add_argument(
        "-w", "--whisper-model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base)"
    )
    parser.add_argument(
        "-m", "--llm-model",
        default="llama3.2",
        help="Ollama model name (default: llama3.2)"
    )
    parser.add_argument(
        "--basic-mode",
        action="store_true",
        help="Use basic processing (disable advanced diarization and LLM enhancement)"
    )
    parser.add_argument(
        "--no-llm-enhancement",
        action="store_true", 
        help="Disable LLM-based speaker role enhancement"
    )
    parser.add_argument(
        "--diarization",
        default="auto",
        choices=["simple", "advanced", "advanced-with-llm-post-processing", "auto"],
        help="Speaker diarization method: simple (pause-based), advanced (pyannote.audio only), advanced-with-llm-post-processing (pyannote.audio + LLM enhancement), auto (advanced if available, fallback to simple)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--activate-license",
        metavar="LICENSE_CODE",
        help="Activate license with the provided license code"
    )
    parser.add_argument(
        "--license-info",
        action="store_true",
        help="Show current license information"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information"
    )
    
    return parser

def handle_lightweight_commands(args):
    """Handle commands that don't require heavy imports"""
    
    # Handle version command (lightweight)
    if args.version:
        print("Blackowiak LLM v1.0.0")
        print("Advanced Therapy Session Processor")
        return 0
    
    # Handle license commands (need license manager but not heavy AI libs)
    if args.activate_license or args.license_info:
        # Import license manager only when needed
        sys.path.append(str(Path(__file__).parent.parent))
        from license_manager import LicenseManager
        
        if args.activate_license:
            license_manager = LicenseManager()
            success, message = license_manager.activate_license(args.activate_license)
            
            if success:
                print("✅ License activated successfully!")
                print(f"   {message}")
            else:
                print("❌ License activation failed")
                print(f"   {message}")
            
            return 0 if success else 1
        
        if args.license_info:
            license_manager = LicenseManager()
            is_licensed, message, license_info = license_manager.check_license()
            
            if is_licensed:
                print("✅ LICENSE INFORMATION")
                print(f"Email: {license_info['email']}")
                print(f"Type: {license_info['type']}")
                print(f"Expires: {license_info['expires']}")
                print(f"Usage count: {license_info['usage_count']}")
            else:
                print("❌ NO VALID LICENSE")
                print(f"   {message}")
            
            return 0
    
    # If we get here, we need to do actual processing
    return None

def main():
    """Main CLI entry point with fast startup for lightweight commands"""
    
    # Parse arguments first (this is very fast)
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle lightweight commands first (no heavy imports)
    result = handle_lightweight_commands(args)
    if result is not None:
        return result
    
    # If we get here, we need heavy processing, so import the full core module
    print("🔄 Loading AI processing libraries...")
    
    # Handle imports for both development and PyInstaller environments
    try:
        # Try PyInstaller bundled import first
        from app.core import process_with_args
    except ImportError:
        # Fall back to development environment import
        from core import process_with_args
    
    # Pass control to the heavy processing module with pre-parsed args
    return process_with_args(args)

if __name__ == "__main__":
    sys.exit(main())
