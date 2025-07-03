#!/usr/bin/env python3
"""
Blackowiak LLM - License Management System

This module handles license validation and enforcement for the commercial version.
"""

import os
import json
import hashlib
import hmac
import base64
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple
import platform
import uuid

class LicenseManager:
    """Handles license generation, validation, and enforcement"""
    
    def __init__(self):
        self.license_file = Path.home() / ".blackowiak-llm" / "license.json"
        self.license_file.parent.mkdir(exist_ok=True)
        
        # This would be your secret key (keep this secure in production)
        self._secret_key = "BLACKOWIAK_LLM_SECRET_2025_SECURE_KEY"
        
    def generate_license_code(self, 
                             customer_email: str,
                             license_type: str = "standard",
                             duration_days: int = 365,
                             max_uses: Optional[int] = None) -> str:
        """
        Generate a license code for a customer
        
        Args:
            customer_email: Customer's email address
            license_type: Type of license (trial, standard, professional)
            duration_days: How many days the license is valid
            max_uses: Maximum number of uses (None for unlimited)
            
        Returns:
            Base64 encoded license code
        """
        
        # Create license data
        license_data = {
            "email": customer_email,
            "type": license_type,
            "issued": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(days=duration_days)).isoformat(),
            "max_uses": max_uses,
            "version": "1.0"
        }
        
        # Create signature
        license_json = json.dumps(license_data, sort_keys=True)
        signature = self._create_signature(license_json)
        
        # Combine license and signature
        license_package = {
            "license": license_data,
            "signature": signature
        }
        
        # Encode as base64 for easy sharing
        license_code = base64.b64encode(
            json.dumps(license_package).encode()
        ).decode()
        
        return license_code
    
    def validate_license_code(self, license_code: str) -> Tuple[bool, str, Dict]:
        """
        Validate a license code
        
        Returns:
            (is_valid, error_message, license_data)
        """
        
        try:
            # Decode license
            license_package = json.loads(
                base64.b64decode(license_code.encode()).decode()
            )
            
            license_data = license_package["license"]
            signature = license_package["signature"]
            
            # Verify signature
            license_json = json.dumps(license_data, sort_keys=True)
            if not self._verify_signature(license_json, signature):
                return False, "Invalid license signature", {}
            
            # Check expiration
            expires = datetime.fromisoformat(license_data["expires"])
            if datetime.now() > expires:
                return False, "License has expired", license_data
            
            # Check usage count if applicable
            if license_data.get("max_uses"):
                usage_count = self._get_usage_count(license_code)
                if usage_count >= license_data["max_uses"]:
                    return False, "License usage limit exceeded", license_data
            
            return True, "Valid license", license_data
            
        except Exception as e:
            return False, f"Invalid license format: {e}", {}
    
    def activate_license(self, license_code: str) -> Tuple[bool, str]:
        """
        Activate a license on this machine
        
        Returns:
            (success, message)
        """
        
        is_valid, error_msg, license_data = self.validate_license_code(license_code)
        
        if not is_valid:
            return False, error_msg
        
        # Store license locally
        machine_id = self._get_machine_id()
        activation_data = {
            "license_code": license_code,
            "license_data": license_data,
            "machine_id": machine_id,
            "activated": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        with open(self.license_file, 'w') as f:
            json.dump(activation_data, f, indent=2)
        
        return True, f"License activated for {license_data['email']}"
    
    def check_license(self) -> Tuple[bool, str, Dict]:
        """
        Check if current machine has valid license
        
        Returns:
            (is_licensed, message, license_info)
        """
        
        if not self.license_file.exists():
            return False, "No license found. Please activate a license.", {}
        
        try:
            with open(self.license_file, 'r') as f:
                activation_data = json.load(f)
            
            # Validate the stored license
            is_valid, error_msg, license_data = self.validate_license_code(
                activation_data["license_code"]
            )
            
            if not is_valid:
                return False, error_msg, {}
            
            # Check machine ID (prevent license sharing)
            current_machine_id = self._get_machine_id()
            if activation_data["machine_id"] != current_machine_id:
                return False, "License is tied to a different machine", {}
            
            return True, "License valid", {
                "type": license_data["type"],
                "email": license_data["email"],
                "expires": license_data["expires"],
                "usage_count": activation_data["usage_count"]
            }
            
        except Exception as e:
            return False, f"License error: {e}", {}
    
    def increment_usage(self):
        """Increment usage counter"""
        if self.license_file.exists():
            try:
                with open(self.license_file, 'r') as f:
                    activation_data = json.load(f)
                
                activation_data["usage_count"] += 1
                activation_data["last_used"] = datetime.now().isoformat()
                
                with open(self.license_file, 'w') as f:
                    json.dump(activation_data, f, indent=2)
                    
            except Exception:
                pass  # Fail silently
    
    def _create_signature(self, data: str) -> str:
        """Create HMAC signature for license data"""
        signature = hmac.new(
            self._secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _verify_signature(self, data: str, signature: str) -> bool:
        """Verify HMAC signature"""
        expected_signature = self._create_signature(data)
        return hmac.compare_digest(expected_signature, signature)
    
    def _get_machine_id(self) -> str:
        """Get unique machine identifier"""
        # Combine multiple machine characteristics
        machine_info = [
            platform.node(),  # Computer name
            platform.machine(),  # Architecture
            platform.processor(),  # Processor
        ]
        
        # Add MAC address if available
        try:
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0,2*6,2)][::-1])
            machine_info.append(mac)
        except:
            pass
        
        # Create hash of machine info
        machine_string = '|'.join(str(info) for info in machine_info)
        machine_id = hashlib.sha256(machine_string.encode()).hexdigest()[:16]
        
        return machine_id
    
    def _get_usage_count(self, license_code: str) -> int:
        """Get current usage count for a license"""
        if self.license_file.exists():
            try:
                with open(self.license_file, 'r') as f:
                    activation_data = json.load(f)
                
                if activation_data.get("license_code") == license_code:
                    return activation_data.get("usage_count", 0)
                    
            except Exception:
                pass
        
        return 0

def license_required(func):
    """Decorator to enforce license checking"""
    def wrapper(*args, **kwargs):
        license_manager = LicenseManager()
        is_licensed, message, license_info = license_manager.check_license()
        
        if not is_licensed:
            print("❌ LICENSE REQUIRED")
            print(f"   {message}")
            print()
            print("To activate your license:")
            print("   python run.py --activate-license YOUR_LICENSE_CODE")
            print()
            print("To purchase a license:")
            print("   Visit: https://blackowiak-llm.com/purchase")
            return 1
        
        # Show license info
        print(f"✅ Licensed to: {license_info['email']}")
        print(f"   License type: {license_info['type']}")
        print(f"   Usage count: {license_info['usage_count']}")
        print()
        
        # Increment usage counter
        license_manager.increment_usage()
        
        # Run the original function
        return func(*args, **kwargs)
    
    return wrapper

# License generation tool (for you as the vendor)
def generate_license_cli():
    """Command line tool for generating licenses"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate license codes")
    parser.add_argument("--email", required=True, help="Customer email")
    parser.add_argument("--type", default="standard", 
                       choices=["trial", "standard", "professional"],
                       help="License type")
    parser.add_argument("--days", type=int, default=365, 
                       help="License duration in days")
    parser.add_argument("--max-uses", type=int, 
                       help="Maximum uses (optional)")
    
    args = parser.parse_args()
    
    license_manager = LicenseManager()
    license_code = license_manager.generate_license_code(
        customer_email=args.email,
        license_type=args.type,
        duration_days=args.days,
        max_uses=args.max_uses
    )
    
    print("LICENSE CODE GENERATED")
    print("=" * 50)
    print(f"Customer: {args.email}")
    print(f"Type: {args.type}")
    print(f"Duration: {args.days} days")
    print(f"Max uses: {args.max_uses or 'Unlimited'}")
    print()
    print("LICENSE CODE:")
    print(license_code)
    print()
    print("Customer activation command:")
    print(f"python run.py --activate-license {license_code}")

if __name__ == "__main__":
    generate_license_cli()
