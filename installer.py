#!/usr/bin/env python3
"""
Blackowiak LLM - Professional Installer Script

This script creates a professional installer experience for customers.
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path
import urllib.request
import zipfile
import tempfile

class BlackowiakLLMInstaller:
    """Professional installer for Blackowiak LLM"""
    
    def __init__(self):
        self.system = platform.system()
        self.install_dir = self._get_install_directory()
        self.app_name = "Blackowiak LLM"
        
    def _get_install_directory(self):
        """Get appropriate installation directory for the OS"""
        if self.system == "Darwin":  # macOS
            return Path.home() / "Applications" / "Blackowiak-LLM"
        elif self.system == "Windows":
            return Path.home() / "AppData" / "Local" / "Blackowiak-LLM"
        else:  # Linux
            return Path.home() / ".local" / "share" / "Blackowiak-LLM"
    
    def welcome_screen(self):
        """Display welcome message"""
        print("=" * 60)
        print("🧠 BLACKOWIAK LLM - PROFESSIONAL INSTALLER")
        print("=" * 60)
        print(f"Welcome to {self.app_name}!")
        print()
        print("This installer will:")
        print("✓ Install Blackowiak LLM to your system")
        print("✓ Set up desktop shortcuts")
        print("✓ Configure system dependencies")
        print("✓ Create sample data and templates")
        print()
        print(f"Installation directory: {self.install_dir}")
        print()
        
        response = input("Continue with installation? (y/N): ").strip().lower()
        return response in ['y', 'yes']
    
    def check_system_requirements(self):
        """Check if system meets requirements"""
        print("🔍 Checking system requirements...")
        
        requirements_met = True
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major == 3 and python_version.minor >= 10:
            print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        else:
            print(f"✗ Python version {python_version.major}.{python_version.minor} (requires 3.10+)")
            requirements_met = False
        
        # Check available disk space
        try:
            statvfs = os.statvfs(str(self.install_dir.parent))
            free_space_gb = (statvfs.f_frsize * statvfs.f_bavail) / (1024**3)
            if free_space_gb >= 2:
                print(f"✓ Disk space: {free_space_gb:.1f}GB available")
            else:
                print(f"✗ Insufficient disk space: {free_space_gb:.1f}GB (requires 2GB+)")
                requirements_met = False
        except:
            print("⚠ Could not check disk space")
        
        # Check for ffmpeg
        ffmpeg_available = shutil.which("ffmpeg") is not None
        if ffmpeg_available:
            print("✓ ffmpeg available")
        else:
            print("⚠ ffmpeg not found (will guide installation)")
        
        # Check for Ollama
        ollama_available = shutil.which("ollama") is not None
        if ollama_available:
            print("✓ Ollama available")
        else:
            print("⚠ Ollama not found (will guide installation)")
        
        return requirements_met
    
    def check_all_dependencies(self):
        """Comprehensive dependency check with installation guidance"""
        print("🔍 Checking all dependencies...")
        
        missing_deps = []
        install_guides = []
        
        # Check Python packages (bundled with binary)
        print("✓ Python packages: Bundled with application")
        
        # Check ffmpeg
        if not shutil.which("ffmpeg"):
            missing_deps.append("ffmpeg")
            if self.system == "Darwin":
                install_guides.append("ffmpeg: brew install ffmpeg")
            elif self.system == "Windows":
                install_guides.append("ffmpeg: Download from https://ffmpeg.org/download.html")
            else:
                install_guides.append("ffmpeg: sudo apt install ffmpeg")
        else:
            print("✓ ffmpeg: Available")
        
        # Check Ollama
        if not shutil.which("ollama"):
            missing_deps.append("Ollama")
            install_guides.append("Ollama: Download from https://ollama.ai/")
        else:
            print("✓ Ollama: Available")
            
            # Check if llama3.2 model is available
            try:
                result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
                if "llama3.2" in result.stdout:
                    print("✓ Ollama model (llama3.2): Available")
                else:
                    missing_deps.append("llama3.2 model")
                    install_guides.append("llama3.2 model: ollama pull llama3.2")
            except:
                print("⚠ Could not check Ollama models")
        
        return missing_deps, install_guides
    
    def install_dependencies(self):
        """Guide user through dependency installation with automation where possible"""
        print("\n🔧 Installing dependencies...")
        
        missing_deps, install_guides = self.check_all_dependencies()
        
        if not missing_deps:
            print("✅ All dependencies are already installed!")
            return True
        
        print(f"\n📋 Missing dependencies: {', '.join(missing_deps)}")
        print("\nChoose installation method:")
        print("1. Automatic installation (recommended)")
        print("2. Manual installation (with guidance)")
        print("3. Skip for now")
        
        choice = input("Enter choice (1/2/3): ").strip()
        
        if choice == "1":
            return self._auto_install_dependencies(missing_deps)
        elif choice == "2":
            self._manual_install_guide(install_guides)
            return True
        else:
            print("⚠ Skipping dependency installation.")
            print("Note: The application may not work until dependencies are installed.")
            return True
    
    def _auto_install_dependencies(self, missing_deps):
        """Attempt automatic installation of dependencies"""
        print("\n🤖 Attempting automatic installation...")
        
        success_count = 0
        total_deps = len(missing_deps)
        
        # Auto-install ffmpeg
        if "ffmpeg" in missing_deps:
            if self._auto_install_ffmpeg():
                success_count += 1
                print("✅ ffmpeg installed successfully")
            else:
                print("❌ ffmpeg installation failed")
        
        # Guide Ollama installation (can't be fully automated)
        if "Ollama" in missing_deps:
            print("\n📥 OLLAMA INSTALLATION")
            print("Ollama must be installed manually:")
            print("1. Visit: https://ollama.ai/")
            print("2. Download and install for your operating system")
            print("3. Restart this installer")
            
            open_browser = input("Open download page in browser? (y/N): ").strip().lower()
            if open_browser in ['y', 'yes']:
                try:
                    import webbrowser
                    webbrowser.open("https://ollama.ai/")
                except:
                    pass
            
            return False  # Need manual intervention
        
        # Auto-install Ollama model
        if "llama3.2 model" in missing_deps and shutil.which("ollama"):
            if self._auto_install_ollama_model():
                success_count += 1
                print("✅ llama3.2 model installed successfully")
            else:
                print("❌ llama3.2 model installation failed")
        
        print(f"\n📊 Installation result: {success_count}/{total_deps} dependencies installed")
        return success_count == total_deps
    
    def _auto_install_ffmpeg(self):
        """Attempt to automatically install ffmpeg"""
        try:
            if self.system == "Darwin":  # macOS
                # Check for Homebrew first
                if shutil.which("brew"):
                    subprocess.run(["brew", "install", "ffmpeg"], check=True)
                    return True
                else:
                    print("❌ Homebrew not found. Please install Homebrew first.")
                    return False
                    
            elif self.system == "Linux":
                # Try different package managers
                if shutil.which("apt-get"):
                    subprocess.run(["sudo", "apt-get", "update"], check=True)
                    subprocess.run(["sudo", "apt-get", "install", "-y", "ffmpeg"], check=True)
                    return True
                elif shutil.which("yum"):
                    subprocess.run(["sudo", "yum", "install", "-y", "ffmpeg"], check=True)
                    return True
                elif shutil.which("dnf"):
                    subprocess.run(["sudo", "dnf", "install", "-y", "ffmpeg"], check=True)
                    return True
                else:
                    return False
            else:  # Windows
                print("❌ Automatic ffmpeg installation not supported on Windows")
                return False
                
        except subprocess.CalledProcessError:
            return False
        except Exception:
            return False
    
    def _auto_install_ollama_model(self):
        """Attempt to automatically install Ollama model"""
        try:
            print("📥 Downloading llama3.2 model (this may take several minutes)...")
            result = subprocess.run(["ollama", "pull", "llama3.2"], check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Model download failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def _manual_install_guide(self, install_guides):
        """Provide manual installation guidance"""
        print("\n📋 MANUAL INSTALLATION GUIDE")
        print("=" * 40)
        
        for guide in install_guides:
            print(f"• {guide}")
        
        print("\n🔄 After installing dependencies, run this installer again.")
        print("📞 Need help? Visit: https://blackowiak-llm.com/support")
    
    def copy_files(self):
        """Copy application files to installation directory"""
        print(f"\n📁 Installing to {self.install_dir}...")
        
        # Create installation directory
        self.install_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy main executable and supporting files
        source_dir = Path(__file__).parent
        
        # Copy the standalone binary (main executable)
        binary_source = source_dir / "blackowiak-llm"
        binary_dest = self.install_dir / "blackowiak-llm"
        
        if binary_source.exists():
            shutil.copy2(binary_source, binary_dest)
            binary_dest.chmod(0o755)  # Make executable
            print("✓ Copied blackowiak-llm (main binary)")
        else:
            print("❌ ERROR: blackowiak-llm binary not found!")
            raise FileNotFoundError("Main binary 'blackowiak-llm' not found in package")
        
        # Copy only the README (minimal installation)
        readme_source = source_dir / "README.md"
        readme_dest = self.install_dir / "README.md"
        
        if readme_source.exists():
            shutil.copy2(readme_source, readme_dest)
            print("✓ Copied README.md")
        else:
            print("⚠ README.md not found in package")
        
        print("✓ Installation complete - minimal files copied (binary + README only)")
    
    def create_shortcuts(self):
        """Create desktop shortcuts and menu entries"""
        print("\n🔗 Creating shortcuts...")
        
        if self.system == "Darwin":  # macOS
            self._create_macos_shortcuts()
        elif self.system == "Windows":
            self._create_windows_shortcuts()
        else:  # Linux
            self._create_linux_shortcuts()
    
    def _create_macos_shortcuts(self):
        """Create macOS shortcuts"""
        # Create symlink in local bin for easy access as 'blackowiak'
        local_bin = Path.home() / ".local" / "bin"
        local_bin.mkdir(parents=True, exist_ok=True)
        
        symlink_path = local_bin / "blackowiak"
        if symlink_path.exists():
            symlink_path.unlink()
        
        try:
            symlink_path.symlink_to(self.install_dir / "blackowiak-llm")
            print("✓ Added 'blackowiak' command to PATH")
            print(f"✓ You can now run: blackowiak --help")
        except Exception as e:
            print(f"⚠ Could not create symlink: {e}")
            print(f"  You can manually run: {self.install_dir}/blackowiak-llm")
        
        # Update shell PATH if needed
        shell_rc = Path.home() / ".zshrc"
        path_line = f'export PATH="$HOME/.local/bin:$PATH"'
        
        if shell_rc.exists():
            content = shell_rc.read_text()
            if "$HOME/.local/bin" not in content:
                shell_rc.write_text(content + f"\n# Added by Blackowiak LLM installer\n{path_line}\n")
                print("✓ Updated shell PATH (restart terminal or run 'source ~/.zshrc')")
        
        print("✓ Installation complete - you can now use 'blackowiak' command")
    
    def _create_windows_shortcuts(self):
        """Create Windows shortcuts"""
        # Create batch file
        launcher_batch = self.install_dir / "Blackowiak-LLM.bat"
        launcher_batch.write_text(f"""@echo off
cd /d "{self.install_dir}"
python run.py %*
pause
""")
        
        print("✓ Created Blackowiak-LLM.bat")
        print(f"  Double-click {launcher_batch} to run")
    
    def _create_linux_shortcuts(self):
        """Create Linux shortcuts"""
        # Create launcher script
        launcher_script = self.install_dir / "blackowiak-llm"
        launcher_script.write_text(f"""#!/bin/bash
cd "{self.install_dir}"
python3 run.py "$@"
""")
        launcher_script.chmod(0o755)
        
        # Try to add to local bin
        local_bin = Path.home() / ".local" / "bin"
        local_bin.mkdir(parents=True, exist_ok=True)
        
        symlink_path = local_bin / "blackowiak-llm"
        if symlink_path.exists():
            symlink_path.unlink()
        symlink_path.symlink_to(launcher_script)
        
        print("✓ Created launcher script")
        print("✓ Added to ~/.local/bin/blackowiak-llm")
    
    def setup_license_activation(self):
        """Guide user through license activation"""
        print("\n🔑 LICENSE ACTIVATION")
        print("=" * 40)
        print("To activate your license, you'll need your license code.")
        print("If you don't have one yet, visit: https://blackowiak-llm.com/purchase")
        print()
        
        license_code = input("Enter your license code (or press Enter to skip): ").strip()
        
        if license_code:
            # Try to activate using the new binary command
            try:
                result = subprocess.run([
                    "blackowiak", "--activate-license", license_code
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ License activated successfully!")
                else:
                    print(f"❌ License activation failed: {result.stderr}")
                    print("You can activate later with:")
                    print(f"  blackowiak --activate-license YOUR_LICENSE_CODE")
            except Exception as e:
                print(f"❌ Error activating license: {e}")
                print("You can activate later with:")
                print(f"  blackowiak --activate-license YOUR_LICENSE_CODE")
    
    def installation_complete(self):
        """Display completion message"""
        print("\n🎉 INSTALLATION COMPLETE!")
        print("=" * 50)
        print(f"{self.app_name} has been successfully installed to:")
        print(f"  {self.install_dir}")
        print()
        print("💻 GETTING STARTED:")
        print("1. Restart your terminal (or run 'source ~/.zshrc')")
        print("2. Run: blackowiak --help")
        print("3. Process your first audio file:")
        print("   blackowiak your_audio_file.wav")
        print()
        print("📚 NEXT STEPS:")
        print("• Install dependencies (Ollama, FFmpeg) - see README.md")
        print("• Activate your license: blackowiak --activate-license YOUR_CODE")
        print("• Read the README.md for complete setup instructions")
        print()
        print("🆘 SUPPORT:")
        print("  Email: support@blackowiak-llm.com")
        print("  Website: https://blackowiak-llm.com/support")
        print()
        print("Thank you for choosing Blackowiak LLM!")
    
    def run_installation(self):
        """Run the complete installation process"""
        try:
            if not self.welcome_screen():
                print("Installation cancelled.")
                return False
            
            if not self.check_system_requirements():
                print("❌ System requirements not met.")
                return False
            
            # Enhanced dependency installation
            if not self.install_dependencies():
                print("⚠ Installation completed with missing dependencies.")
                print("The application may not work until all dependencies are installed.")
                print("Run this installer again after installing missing dependencies.")
            
            self.copy_files()
            self.create_shortcuts()
            self.setup_license_activation()
            self.installation_complete()
            
            return True
            
        except KeyboardInterrupt:
            print("\n\nInstallation cancelled by user.")
            return False
        except Exception as e:
            print(f"\n❌ Installation failed: {e}")
            return False

def main():
    """Main installer entry point"""
    installer = BlackowiakLLMInstaller()
    success = installer.run_installation()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
