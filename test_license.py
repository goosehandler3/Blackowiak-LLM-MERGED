#!/usr/bin/env python3
"""
Quick test of license system
"""

from license_manager import LicenseManager

# Generate a test license
license_manager = LicenseManager()

print("1. Generating test license...")
license_code = license_manager.generate_license_code(
    customer_email="test@example.com",
    license_type="trial",
    duration_days=30,
    max_uses=5
)
print(f"License code: {license_code[:50]}...")

print("\n2. Activating license...")
success, message = license_manager.activate_license(license_code)
print(f"Activation: {success} - {message}")

print("\n3. Checking license...")
is_licensed, check_message, license_info = license_manager.check_license()
print(f"License valid: {is_licensed}")
if is_licensed:
    print(f"Email: {license_info['email']}")
    print(f"Type: {license_info['type']}")
    print(f"Usage: {license_info['usage_count']}")

print("\n4. Testing usage increment...")
license_manager.increment_usage()

print("\n5. Checking usage after increment...")
is_licensed, check_message, license_info = license_manager.check_license()
if is_licensed:
    print(f"Usage after increment: {license_info['usage_count']}")

print("\n✅ License system test completed!")
