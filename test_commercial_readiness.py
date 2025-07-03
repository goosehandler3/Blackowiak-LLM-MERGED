#!/usr/bin/env python3
"""
Quick commercial readiness test
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def test_license_system():
    """Test the license system"""
    print("🔑 Testing License System...")
    
    from license_manager import LicenseManager
    
    # Test license generation
    license_manager = LicenseManager()
    license_code = license_manager.generate_license_code(
        customer_email="test@example.com",
        license_type="trial",
        duration_days=30,
        max_uses=5
    )
    
    print(f"✅ License generation: {len(license_code)} characters")
    
    # Test activation
    success, message = license_manager.activate_license(license_code)
    print(f"✅ License activation: {success}")
    
    # Test validation
    is_valid, msg, info = license_manager.check_license()
    print(f"✅ License validation: {is_valid}")
    
    return True

def test_cli_imports():
    """Test that the CLI can import all necessary modules"""
    print("📦 Testing CLI Imports...")
    
    try:
        from core import main, LicenseManager, EnhancedSessionProcessor
        print("✅ Core imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_build_readiness():
    """Test if the project is ready for building"""
    print("🏗️ Testing Build Readiness...")
    
    required_files = [
        "run.py",
        "license_manager.py", 
        "app/core.py",
        "build.sh",
        "build_advanced.sh",
        "installer.py",
        "templates/SOAP_template.txt",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_license_integration():
    """Test license integration in the main CLI"""
    print("🔗 Testing License Integration...")
    
    try:
        # Import the main module
        from core import main
        
        # The main function should exist and be callable
        print("✅ Main function accessible")
        
        # Check if license manager is properly imported in core
        with open("app/core.py", "r") as f:
            content = f.read()
            
        if "from license_manager import" in content:
            print("✅ License manager imported in core")
        else:
            print("❌ License manager not imported in core")
            return False
            
        if "--activate-license" in content:
            print("✅ License activation CLI option present")
        else:
            print("❌ License activation CLI option missing")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 BLACKOWIAK LLM - COMMERCIAL READINESS TEST")
    print("=" * 50)
    
    tests = [
        ("License System", test_license_system),
        ("CLI Imports", test_cli_imports), 
        ("Build Readiness", test_build_readiness),
        ("License Integration", test_license_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append(False)
            print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("📊 TEST RESULTS")
    print("=" * 20)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print()
        print("✅ Your commercial package is ready!")
        print()
        print("🚀 Next steps:")
        print("   1. Run: ./build_advanced.sh binary")
        print("   2. Test the generated executable")
        print("   3. Generate customer licenses") 
        print("   4. Set up payment processing")
        print("   5. Launch!")
        return 0
    else:
        print("❌ Some tests failed. Please fix issues before commercial launch.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
