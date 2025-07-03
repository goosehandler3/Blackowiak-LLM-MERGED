from cx_Freeze import setup, Executable
import sys

# Include files
include_files = [
    ("templates/", "templates/"),
    ("example_data/", "example_data/"),
    ("license_manager.py", "license_manager.py"),
    ("version_info.py", "version_info.py"),
]

# Build options
build_options = {
    "packages": ["whisper", "torch", "requests", "rich", "pydub", "librosa"],
    "include_files": include_files,
    "excludes": ["tkinter", "matplotlib"],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": [],
}

# Executable
executables = [
    Executable(
        "run.py",
        base="Console",
        target_name="blackowiak-llm-v1.0.0.exe",
        icon=None
    )
]

setup(
    name="Blackowiak LLM",
    version="1.0.0",
    description="AI-Powered Therapy Session Processor",
    author="Andrew Blackowiak",
    options={"build_exe": build_options},
    executables=executables
)
