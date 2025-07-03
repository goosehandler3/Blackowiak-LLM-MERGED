#!/usr/bin/env python3
"""
Test script to verify Blackowiak LLM installation and dependencies
"""

import sys
import os
from pathlib import Path

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def test_core_imports():
    """Test if core dependencies can be imported"""
    print("\n📦 Testing core dependencies...")
    
    required_modules = [
        ("whisper", "OpenAI Whisper"),
        ("torch", "PyTorch"),
        ("requests", "Requests"),
        ("rich", "Rich console"),
        ("pydub", "PyDub audio processing"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas")
    ]
    
    all_good = True
    
    for module_name, display_name in required_modules:
        try:
            __import__(module_name)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name} - Not installed")
            all_good = False
    
    return all_good

def test_ollama_connection():
    """Test connection to Ollama"""
    print("\n🤖 Testing Ollama connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama is running with {len(models)} models")
            for model in models[:3]:  # Show first 3 models
                print(f"   - {model['name']}")
            return True
        else:
            print("❌ Ollama is running but returned an error")
            return False
    except ImportError:
        print("❌ Cannot test Ollama - requests module not available")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Ollama is not running")
        print("   Install Ollama: https://ollama.ai/")
        print("   Then run: ollama pull llama3.2")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return False

def test_file_structure():
    """Test if required files and directories exist"""
    print("\n📁 Testing file structure...")
    
    required_items = [
        ("app/core.py", "Core processing module"),
        ("requirements.txt", "Requirements file"),
        ("templates/SOAP_template.txt", "SOAP template"),
        ("example_data/", "Example data directory")
    ]
    
    all_good = True
    base_path = Path(__file__).parent
    
    for item_path, description in required_items:
        full_path = base_path / item_path
        if full_path.exists():
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - Missing: {item_path}")
            all_good = False
    
    return all_good

def test_audio_processing():
    """Test basic audio processing capabilities"""
    print("\n🎵 Testing audio processing...")
    
    try:
        import whisper
        # Just test model loading, don't actually load it (too slow)
        available_models = whisper.available_models()
        print(f"✅ Whisper available with models: {', '.join(list(available_models)[:3])}...")
        return True
    except ImportError:
        print("❌ Whisper not available")
        return False
    except Exception as e:
        print(f"❌ Error testing audio processing: {e}")
        return False

def main():
    """Run all tests"""
    print("🧠 Blackowiak LLM - Installation Test")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_file_structure,
        test_core_imports,
        test_audio_processing,
        test_ollama_connection
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All tests passed ({passed}/{total})")
        print("\n🎉 Your Blackowiak LLM installation is ready!")
        print("\nNext steps:")
        print("1. Place an audio file in the project directory")
        print("2. Run: python run.py your_audio_file.wav")
        print("3. Check the output/ directory for results")
        return 0
    else:
        print(f"❌ {total - passed} tests failed ({passed}/{total} passed)")
        print("\n🔧 Please fix the issues above before using the system.")
        
        if not results[2]:  # Core imports failed
            print("\nTo install missing dependencies:")
            print("pip install -r requirements.txt")
        
        if not results[4]:  # Ollama failed
            print("\nTo set up Ollama:")
            print("1. Download from: https://ollama.ai/")
            print("2. Run: ollama pull llama3.2")
        
        return 1

if __name__ == "__main__":
    exit(main())
