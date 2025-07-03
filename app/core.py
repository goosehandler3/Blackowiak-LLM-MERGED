#!/usr/bin/env python3
"""
Blackowiak LLM - Core Audio Processing Module

This module handles the core functionality of processing therapy session audio files:
1. Audio transcription with speaker diarization
2. LLM-based session summary generation
3. Clinical note generation (SOAP format)
"""

import os
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Lazy imports - only load heavy libraries when needed
# This dramatically improves startup time for --help, --version, etc.

# Light imports only
import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

# Import license manager
import sys
sys.path.append(str(Path(__file__).parent.parent))
from license_manager import LicenseManager, license_required

# Global variables for lazy-loaded modules
_whisper = None
_torch = None
_pyannote_pipeline = None
_AudioSegment = None
PYANNOTE_AVAILABLE = None

def _lazy_import_audio_libs():
    """Lazy import of heavy audio processing libraries"""
    global _whisper, _torch, _pyannote_pipeline, _AudioSegment, PYANNOTE_AVAILABLE
    
    if _whisper is None:
        console.print("🔄 Loading AI libraries (this may take a moment)...", style="yellow")
        
        # Import whisper
        import whisper
        _whisper = whisper
        
        # Import torch
        import torch
        _torch = torch
        
        # Import audio processing
        from pydub import AudioSegment
        _AudioSegment = AudioSegment
        
        # Try to import pyannote
        try:
            from pyannote.audio import Pipeline
            _pyannote_pipeline = Pipeline
            PYANNOTE_AVAILABLE = True
        except ImportError:
            PYANNOTE_AVAILABLE = False
            console.print("Note: pyannote.audio not available. Using basic speaker diarization.", style="dim")
    
    return _whisper, _torch, _pyannote_pipeline, _AudioSegment, PYANNOTE_AVAILABLE

# Initialize rich console for better CLI output
console = Console()

class AdvancedAudioProcessor:
    """Enhanced AudioProcessor with pyannote.audio speaker diarization and LLM enhancement"""
    
    def __init__(self, whisper_model: str = "base", use_pyannote: bool = True, use_llm_enhancement: bool = True):
        """
        Initialize the advanced audio processor
        
        Args:
            whisper_model: Whisper model size ("tiny", "base", "small", "medium", "large")
            use_pyannote: Whether to use pyannote.audio for advanced diarization
            use_llm_enhancement: Whether to use LLM for post-processing speaker roles
        """
        self.whisper_model = whisper_model
        self.whisper = None
        self.diarization_pipeline = None
        self.use_pyannote = use_pyannote  # Don't check availability here
        self.use_llm_enhancement = use_llm_enhancement
        self._libs_loaded = False
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _ensure_libs_loaded(self):
        """Ensure heavy libraries are loaded before processing"""
        if not self._libs_loaded:
            # Load heavy libraries on first use
            self.whisper_lib, self.torch_lib, self.Pipeline, self.AudioSegment, self.pyannote_available = _lazy_import_audio_libs()
            self._libs_loaded = True
            
            # Now we can check if pyannote is actually available
            self.use_pyannote = self.use_pyannote and self.pyannote_available
            
            if self.use_pyannote:
                self._load_pyannote_pipeline()
        
    def _load_pyannote_pipeline(self):
        """Load pyannote.audio diarization pipeline - ALL PROCESSING IS LOCAL"""
        try:
            console.print("🔄 Loading advanced speaker diarization...", style="yellow")
            console.print("🔒 Privacy: All audio processing happens locally", style="dim")
            
            # Handle PyInstaller environment - set up cache directories
            import os
            import sys
            
            # Check if running in PyInstaller bundle
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                # Running in PyInstaller bundle
                console.print("   Detected PyInstaller environment", style="dim")
                
                # Set up cache directories for PyInstaller
                bundle_dir = getattr(sys, '_MEIPASS', None)
                if bundle_dir:
                    user_cache = os.path.expanduser("~/.cache/huggingface")
                
                # Create cache directory if it doesn't exist
                os.makedirs(user_cache, exist_ok=True)
                
                # Set environment variables for Hugging Face
                os.environ['HF_HOME'] = user_cache
                os.environ['TRANSFORMERS_CACHE'] = user_cache
                os.environ['HF_DATASETS_CACHE'] = user_cache
                
                console.print(f"   Using cache directory: {user_cache}", style="dim")
            
            # Try multiple model loading strategies
            model_attempts = [
                # First try without auth token (works for most public models)
                {"model": "pyannote/speaker-diarization-3.1", "use_auth_token": False},
                # Fallback to older model that definitely doesn't need auth
                {"model": "pyannote/speaker-diarization", "use_auth_token": False},
                # Last resort with auth if available
                {"model": "pyannote/speaker-diarization-3.1", "use_auth_token": True},
            ]
            
            for attempt in model_attempts:
                try:
                    console.print(f"   Trying model: {attempt['model']}", style="dim")
                    
                    # Add debug info about environment
                    if getattr(sys, 'frozen', False):
                        console.print(f"   PyInstaller bundle: {bundle_dir}", style="dim")
                        console.print(f"   HF cache: {os.environ.get('HF_HOME', 'not set')}", style="dim")
                    
                    self.diarization_pipeline = self.Pipeline.from_pretrained(
                        attempt["model"],
                        use_auth_token=attempt["use_auth_token"]
                    )
                    console.print(f"✅ Loaded model: {attempt['model']}", style="green")
                    break
                except Exception as e:
                    console.print(f"   Failed: {str(e)[:100]}...", style="dim red")
                    # Print more details about the error for debugging
                    if "auth" in str(e).lower() or "token" in str(e).lower():
                        console.print("   → This model may require authentication", style="dim yellow")
                    elif "offline" in str(e).lower() or "connection" in str(e).lower():
                        console.print("   → Network/offline issue - this is normal for bundled apps", style="dim yellow")
                    continue
            else:
                # If all attempts failed
                raise Exception("All model loading attempts failed")
            
            # Move to GPU if available for faster LOCAL processing
            if self.torch_lib.cuda.is_available():
                self.diarization_pipeline = self.diarization_pipeline.to(self.torch_lib.device("cuda"))
                console.print("🚀 Using GPU acceleration for LOCAL diarization", style="green")
            
            console.print("✅ Advanced speaker diarization loaded (LOCAL)", style="green")
            console.print("💾 Models cached locally, no internet needed for processing", style="dim")
            
        except Exception as e:
            error_msg = str(e)
            console.print(f"❌ Could not load advanced speaker diarization", style="red")
            
            # Provide user-friendly guidance based on error type
            if "auth" in error_msg.lower() or "token" in error_msg.lower():
                console.print("", style="")
                console.print("� AUTHENTICATION REQUIRED", style="bold yellow")
                console.print("Advanced speaker diarization requires a free Hugging Face account:", style="yellow")
                console.print("", style="")
                console.print("SETUP STEPS:", style="bold")
                console.print("1. Create account: https://huggingface.co/join", style="dim")
                console.print("2. Get access token: https://huggingface.co/settings/tokens", style="dim")
                console.print("3. Accept model license: https://huggingface.co/pyannote/speaker-diarization-3.1", style="dim")
                console.print("4. Login: huggingface-cli login", style="dim")
                console.print("   OR set: export HF_TOKEN='your_token'", style="dim")
                console.print("", style="")
                console.print("💡 This is only needed once - models cache locally for offline use", style="dim cyan")
                console.print("🔒 All processing happens on your computer, not in the cloud", style="dim cyan")
                
            elif "connection" in error_msg.lower() or "network" in error_msg.lower():
                console.print("", style="")
                console.print("🌐 INTERNET CONNECTION REQUIRED", style="bold yellow")
                console.print("First-time setup requires internet to download AI models:", style="yellow")
                console.print("", style="")
                console.print("• Models download once and cache locally", style="dim")
                console.print("• After initial setup, internet is not required", style="dim")
                console.print("• Please connect to internet and try again", style="dim")
                
            elif "offline" in error_msg.lower():
                console.print("", style="")
                console.print("📡 MODELS NOT DOWNLOADED YET", style="bold yellow")
                console.print("Advanced diarization models need to be downloaded first:", style="yellow")
                console.print("", style="")
                console.print("• Connect to internet for first-time setup", style="dim")
                console.print("• Models cache locally for offline use", style="dim")
                
            else:
                console.print("", style="")
                console.print("💭 GENERAL SETUP ISSUE", style="bold yellow")
                console.print("Advanced diarization may need setup:", style="yellow")
                console.print("", style="")
                console.print("TROUBLESHOOTING:", style="bold")
                console.print("1. Ensure internet connection for model download", style="dim")
                console.print("2. Create Hugging Face account if needed", style="dim")
                console.print("3. Run: huggingface-cli login", style="dim")
                console.print("4. Contact support if issues persist", style="dim")
                console.print(f"   Error details: {error_msg[:100]}...", style="dim red")
            
            console.print("", style="")
            console.print("⚡ FALLING BACK TO BASIC DIARIZATION", style="bold green")
            console.print("• Processing will continue with basic speaker detection", style="dim green")
            console.print("• Results will be good but less detailed", style="dim green")
            console.print("", style="")
            
            self.use_pyannote = False
            
    def load_models(self):
        """Load Whisper model"""
        # Ensure libraries are loaded first
        self._ensure_libs_loaded()
        
        console.print("🔄 Loading AI models...", style="yellow")
        
        # Load Whisper model
        with console.status("[bold green]Loading Whisper model..."):
            self.whisper = self.whisper_lib.load_model(self.whisper_model)
        
        console.print("✅ Models loaded successfully!", style="green")
        
    def process_audio(self, audio_path: str) -> Dict:
        """
        Process audio file with advanced speaker diarization
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dictionary containing transcript and enhanced speaker information
        """
        # Ensure libraries are loaded before processing
        self._ensure_libs_loaded()
        
        if not self.whisper:
            self.load_models()
            
        console.print(f"🎵 Processing audio file: {audio_path}", style="blue")
        
        try:
            # Convert audio to format suitable for processing
            audio_segment = self.AudioSegment.from_file(audio_path)
        except Exception as e:
            if "ffmpeg" in str(e).lower():
                console.print("❌ FFMPEG NOT FOUND", style="bold red")
                console.print("Audio processing requires FFmpeg to handle various audio formats.", style="red")
                console.print("", style="")
                console.print("🔧 INSTALLATION:", style="bold green")
                console.print("macOS:     brew install ffmpeg", style="dim")
                console.print("Ubuntu:    sudo apt-get install ffmpeg", style="dim")
                console.print("Windows:   Download from https://ffmpeg.org/", style="dim")
                console.print("", style="")
                console.print("💡 FFmpeg is free and handles all audio/video formats", style="dim cyan")
                console.print("", style="")
                raise Exception("FFmpeg is required for audio processing. Please install it and try again.")
            else:
                console.print(f"❌ Error loading audio file: {e}", style="red")
                console.print("", style="")
                console.print("💡 TROUBLESHOOTING:", style="bold yellow")
                console.print("• Ensure the file exists and is accessible", style="dim")
                console.print("• Check that the file is a valid audio format", style="dim")
                console.print("• Supported formats: MP3, WAV, M4A, MP4, etc.", style="dim")
                console.print("", style="")
                raise Exception(f"Error loading audio file: {e}")
        
        # Export as WAV for processing
        temp_wav = "temp_audio.wav"
        try:
            audio_segment.export(temp_wav, format="wav")
        except Exception as e:
            if "ffmpeg" in str(e).lower():
                console.print("❌ FFMPEG ERROR DURING CONVERSION", style="bold red")
                console.print("FFmpeg encountered an issue converting your audio file.", style="red")
                console.print("", style="")
                console.print("🔧 SOLUTIONS:", style="bold green")
                console.print("1. Reinstall FFmpeg: brew install ffmpeg", style="dim")
                console.print("2. Try a different audio format (WAV, MP3)", style="dim")
                console.print("3. Check if file is corrupted", style="dim")
                console.print("", style="")
                raise Exception("FFmpeg conversion failed. Please check your audio file and FFmpeg installation.")
            else:
                console.print(f"❌ Audio conversion failed: {e}", style="red")
                console.print("", style="")
                console.print("💡 Try converting to WAV format first", style="dim cyan")
                console.print("", style="")
                raise Exception(f"Error converting audio: {e}")
        
        try:
            # Step 1: Transcribe with Whisper
            with console.status("[bold green]Transcribing audio..."):
                if self.whisper is not None:
                    result = self.whisper.transcribe(temp_wav)
                else:
                    raise Exception("Whisper model not loaded")
            
            # Step 2: Advanced speaker diarization
            if self.use_pyannote and self.diarization_pipeline is not None:
                segments = self._pyannote_diarization(temp_wav, result)
            else:
                segments = self._simple_speaker_diarization(audio_segment, result)
            
            # Clean up temp file
            os.remove(temp_wav)
            
            return {
                "transcript": result["text"],
                "segments": segments,
                "language": result.get("language", "en"),
                "duration": len(audio_segment) / 1000.0,
                "diarization_method": "pyannote" if self.use_pyannote else "simple"
            }
            
        except Exception as e:
            self.logger.error(f"Error processing audio: {e}")
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
            raise
    
    def _pyannote_diarization(self, audio_path: str, whisper_result: Dict) -> List[Dict]:
        """Advanced speaker diarization using pyannote.audio"""
        console.print("🧠 Running advanced speaker diarization...", style="blue")
        
        try:
            # Run diarization pipeline
            with console.status("[bold green]Analyzing speakers..."):
                if self.diarization_pipeline is not None:
                    diarization = self.diarization_pipeline(audio_path)
                else:
                    raise Exception("Diarization pipeline not loaded")
            
            # Convert pyannote output to our format
            segments = []
            speaker_map = {}
            speaker_counter = 0
            
            # Map speakers to therapist/client labels (heuristic)
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                if speaker not in speaker_map:
                    if speaker_counter == 0:
                        speaker_map[speaker] = "Therapist"
                    elif speaker_counter == 1:
                        speaker_map[speaker] = "Client"
                    else:
                        speaker_map[speaker] = f"Speaker_{speaker_counter + 1}"
                    speaker_counter += 1
            
            # Align diarization with Whisper segments
            for whisper_segment in whisper_result["segments"]:
                start_time = whisper_segment["start"]
                end_time = whisper_segment["end"]
                text = whisper_segment["text"].strip()
                
                # Find overlapping speaker from diarization
                segment_center = (start_time + end_time) / 2
                best_speaker = "Unknown"
                
                for turn, _, speaker in diarization.itertracks(yield_label=True):
                    if turn.start <= segment_center <= turn.end:
                        best_speaker = speaker_map.get(speaker, f"Speaker_{speaker}")
                        break
                
                segments.append({
                    "start": start_time,
                    "end": end_time,
                    "text": text,
                    "speaker": best_speaker,
                    "confidence": 1.0 - whisper_segment.get("no_speech_prob", 0.0)
                })
            
            console.print(f"✅ Identified {len(speaker_map)} speakers", style="green")
            return segments
            
        except Exception as e:
            console.print(f"❌ Pyannote diarization failed: {e}", style="red")
            console.print("Falling back to simple diarization", style="yellow")
            # Fallback to simple method
            self._ensure_libs_loaded()  # Make sure libs are loaded
            return self._simple_speaker_diarization(
                self.AudioSegment.from_file(audio_path), whisper_result
            )
    
    def _simple_speaker_diarization(self, audio_segment, whisper_result: Dict) -> List[Dict]:
        """
        Simple speaker diarization based on silence detection and speaker changes
        
        This is a basic implementation. For production use, consider:
        - pyannote.audio with proper models
        - speechbrain speaker embeddings
        - More sophisticated voice activity detection
        """
        segments = []
        
        # Use Whisper's segment information
        if "segments" in whisper_result:
            current_speaker = "Therapist"  # Default first speaker
            
            for i, segment in enumerate(whisper_result["segments"]):
                # Simple heuristic: alternate speakers on longer pauses
                if i > 0:
                    prev_end = whisper_result["segments"][i-1]["end"]
                    current_start = segment["start"]
                    pause_duration = current_start - prev_end
                    
                    # If pause is longer than 2 seconds, assume speaker change
                    if pause_duration > 2.0:
                        current_speaker = "Client" if current_speaker == "Therapist" else "Therapist"
                
                segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip(),
                    "speaker": current_speaker,
                    "confidence": 1.0 - segment.get("no_speech_prob", 0.0)
                })
        
        return segments

class LLMEnhancedDiarization:
    """Use LLM to improve speaker diarization post-processing"""
    
    def __init__(self, llm_processor):
        self.llm_processor = llm_processor
    
    def enhance_diarization(self, segments: List[Dict]) -> List[Dict]:
        """Use LLM to improve speaker identification"""
        
        if not segments or len(segments) < 2:
            return segments
        
        console.print("🔍 Enhancing speaker identification with LLM...", style="blue")
        
        # Group segments by speaker for analysis
        speaker_groups = {}
        for segment in segments:
            speaker = segment["speaker"]
            if speaker not in speaker_groups:
                speaker_groups[speaker] = []
            speaker_groups[speaker].append(segment)
        
        # Only enhance if we have 2 speakers (typical therapy session)
        if len(speaker_groups) != 2:
            console.print(f"⚠️  Expected 2 speakers, found {len(speaker_groups)}. Skipping LLM enhancement.", style="yellow")
            return segments
        
        # Analyze each speaker's communication patterns
        speaker_analysis = {}
        for speaker, speaker_segments in speaker_groups.items():
            analysis = self._analyze_speaker_patterns(speaker_segments)
            speaker_analysis[speaker] = analysis
        
        # Use LLM to determine roles
        role_assignments = self._llm_determine_roles(speaker_analysis)
        
        # Apply role assignments
        enhanced_segments = []
        for segment in segments:
            enhanced_segment = segment.copy()
            original_speaker = segment["speaker"]
            enhanced_segment["speaker"] = role_assignments.get(original_speaker, original_speaker)
            enhanced_segment["original_speaker_id"] = original_speaker
            enhanced_segment["llm_enhanced"] = True
            enhanced_segments.append(enhanced_segment)
        
        console.print("✅ Speaker identification enhanced", style="green")
        return enhanced_segments
    
    def _analyze_speaker_patterns(self, segments: List[Dict]) -> Dict:
        """Analyze speech patterns for a single speaker"""
        texts = [seg["text"] for seg in segments]
        combined_text = " ".join(texts)
        
        total_duration = sum(seg["end"] - seg["start"] for seg in segments)
        avg_segment_length = len(combined_text.split()) / len(segments) if segments else 0
        
        # Count questions (simple heuristic)
        question_count = combined_text.count("?")
        
        return {
            "total_segments": len(segments),
            "total_duration": total_duration,
            "total_words": len(combined_text.split()),
            "avg_segment_length": avg_segment_length,
            "question_count": question_count,
            "sample_text": combined_text[:500],  # First 500 chars for analysis
        }
    
    def _llm_determine_roles(self, speaker_analysis: Dict) -> Dict:
        """Use LLM to determine speaker roles based on patterns"""
        
        # Create analysis prompt
        analysis_text = self._format_speaker_analysis(speaker_analysis)
        
        prompt = f"""You are analyzing a therapy session transcript to identify speaker roles.

Speaker Analysis:
{analysis_text}

Based on the speech patterns, communication style, and content themes, determine which speaker is most likely:
1. The THERAPIST (professional, asks questions, provides guidance, uses clinical language)
2. The CLIENT (personal sharing, emotional expression, responds to questions)

Consider factors like:
- Speech volume and frequency
- Question-asking patterns  
- Professional vs personal language
- Topic initiation vs response patterns

Respond with ONLY the speaker assignments in this exact format:
Speaker_1: Therapist
Speaker_2: Client

Or:
Speaker_1: Client  
Speaker_2: Therapist"""

        try:
            response = self.llm_processor._call_ollama(prompt)
            
            # Parse simple response format
            assignments = {}
            for line in response.strip().split('\n'):
                if ':' in line:
                    speaker, role = line.split(':', 1)
                    speaker = speaker.strip()
                    role = role.strip()
                    if role in ['Therapist', 'Client']:
                        assignments[speaker] = role
            
            if len(assignments) == 2:
                console.print(f"🎯 LLM role assignment: {assignments}", style="dim")
                return assignments
            else:
                console.print("⚠️  LLM response format unexpected, using fallback", style="yellow")
                return self._fallback_role_assignment(speaker_analysis)
                
        except Exception as e:
            console.print(f"⚠️  LLM role assignment failed: {e}", style="yellow")
            return self._fallback_role_assignment(speaker_analysis)
    
    def _format_speaker_analysis(self, speaker_analysis: Dict) -> str:
        """Format speaker analysis for LLM prompt"""
        analysis_lines = []
        
        for speaker, stats in speaker_analysis.items():
            analysis_lines.append(f"""
{speaker}:
- Total segments: {stats['total_segments']}
- Speaking time: {stats['total_duration']:.1f} seconds  
- Total words: {stats['total_words']}
- Average words per segment: {stats['avg_segment_length']:.1f}
- Questions asked: {stats['question_count']}
- Sample text: "{stats['sample_text']}"
""")
        
        return "\n".join(analysis_lines)
    
    def _fallback_role_assignment(self, speaker_analysis: Dict) -> Dict:
        """Fallback role assignment using simple heuristics"""
        speakers = list(speaker_analysis.keys())
        if len(speakers) < 2:
            return {}
        
        # Heuristic: Speaker who asks more questions is likely the therapist
        speaker_scores = {}
        for speaker, stats in speaker_analysis.items():
            # Score based on questions asked and speaking pattern
            question_ratio = stats['question_count'] / max(stats['total_words'], 1)
            avg_segment_ratio = stats['avg_segment_length'] / max(stats['total_words'], 1)
            
            # Therapists tend to ask more questions and have shorter, more focused segments
            score = question_ratio * 2 + (1 - avg_segment_ratio)
            speaker_scores[speaker] = score
        
        # Assign roles based on scores
        sorted_speakers = sorted(speaker_scores.keys(), key=lambda x: speaker_scores[x], reverse=True)
        
        return {
            sorted_speakers[0]: "Therapist",  # Higher score (more questions)
            sorted_speakers[1]: "Client"     # Lower score (longer responses)
        }

# Update the original AudioProcessor to maintain backwards compatibility
class AudioProcessor(AdvancedAudioProcessor):
    """Backwards compatible AudioProcessor"""
    
    def __init__(self, whisper_model: str = "base"):
        # Initialize with advanced features but fallback gracefully  
        super().__init__(whisper_model, use_pyannote=True, use_llm_enhancement=False)

class LLMProcessor:
    """Handles LLM interactions for generating session summaries and clinical notes"""
    
    def __init__(self, model_name: str = "llama3.2", ollama_host: str = "http://localhost:11434"):
        """
        Initialize LLM processor
        
        Args:
            model_name: Name of the Ollama model to use
            ollama_host: Ollama server URL
        """
        self.model_name = model_name
        self.ollama_host = ollama_host
        self.logger = logging.getLogger(__name__)
        
    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags")
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
    
    def generate_session_summary(self, transcript_data: Dict) -> Dict:
        """
        Generate a therapy session summary from transcript data
        
        Args:
            transcript_data: Dictionary containing transcript and speaker information
            
        Returns:
            Dictionary containing session summary and clinical notes
        """
        if not self.check_ollama_connection():
            console.print("❌ OLLAMA NOT AVAILABLE", style="bold red")
            console.print("AI-powered session summaries require Ollama to be installed and running.", style="red")
            console.print("", style="")
            console.print("🚀 QUICK SETUP:", style="bold green")
            console.print("1. Install Ollama: https://ollama.ai/", style="dim")
            console.print("2. Download model: ollama pull llama3.2", style="dim")
            console.print("3. Ollama runs automatically after install", style="dim")
            console.print("", style="")
            console.print("💡 After setup, your audio will still be transcribed", style="dim cyan")
            console.print("   but you'll get basic output without AI summaries", style="dim cyan")
            console.print("", style="")
            console.print("⚡ CONTINUING WITH BASIC TRANSCRIPTION", style="bold yellow")
            console.print("", style="")
            return {"error": "Ollama not available", "user_friendly": True}
        
        console.print("🤖 Generating session summary with local LLM...", style="blue")
        
        # Prepare the transcript for LLM processing
        formatted_transcript = self._format_transcript_for_llm(transcript_data)
        
        # Generate session summary
        summary_prompt = self._create_summary_prompt(formatted_transcript)
        summary = self._call_ollama(summary_prompt)
        
        # Generate SOAP note
        soap_prompt = self._create_soap_prompt(formatted_transcript, summary)
        soap_note = self._call_ollama(soap_prompt)
        
        return {
            "session_summary": summary,
            "soap_note": soap_note,
            "transcript_formatted": formatted_transcript,
            "processing_timestamp": datetime.now().isoformat()
        }
    
    def _format_transcript_for_llm(self, transcript_data: Dict) -> str:
        """Format transcript data for LLM processing"""
        if "segments" not in transcript_data:
            return transcript_data.get("transcript", "")
        
        formatted_lines = []
        for segment in transcript_data["segments"]:
            timestamp = f"[{segment['start']:.1f}s]"
            speaker = segment["speaker"]
            text = segment["text"]
            formatted_lines.append(f"{timestamp} {speaker}: {text}")
        
        return "\n".join(formatted_lines)
    
    def _create_summary_prompt(self, transcript: str) -> str:
        """Create prompt for session summary generation"""
        return f"""You are an experienced clinical therapist analyzing a therapy session transcript. 
Please provide a comprehensive but concise summary of this therapy session.

Focus on:
- Key themes and topics discussed
- Client's emotional state and presentation
- Therapeutic interventions used
- Progress made during the session
- Areas for future exploration

Transcript:
{transcript}

Session Summary:"""
    
    def _create_soap_prompt(self, transcript: str, summary: str) -> str:
        """Create prompt for SOAP note generation"""
        return f"""Based on the following therapy session transcript and summary, create a professional SOAP note.

Transcript:
{transcript}

Session Summary:
{summary}

Please format as a standard SOAP note:

SUBJECTIVE: (Client's reported experience, mood, concerns)

OBJECTIVE: (Observable behaviors, presentation, interaction style)

ASSESSMENT: (Clinical impressions, progress, areas of concern)

PLAN: (Next steps, interventions, homework, future goals)"""
    
    def _call_ollama(self, prompt: str) -> str:
        """Make API call to Ollama"""
        try:
            with console.status("[bold green]Thinking..."):
                response = requests.post(
                    f"{self.ollama_host}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=300  # 5 minute timeout
                )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                self.logger.error(f"Ollama API error: {response.status_code}")
                return f"Error: Unable to generate response (Status: {response.status_code})"
                
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Try with a smaller model or shorter transcript."
        except Exception as e:
            self.logger.error(f"Error calling Ollama: {e}")
            return f"Error: {str(e)}"

class SessionProcessor:
    """Main class that orchestrates the entire session processing pipeline"""
    
    def __init__(self, whisper_model: str = "base", llm_model: str = "llama3.2"):
        """
        Initialize the session processor
        
        Args:
            whisper_model: Whisper model size
            llm_model: Ollama model name
        """
        self.audio_processor = AudioProcessor(whisper_model)
        self.llm_processor = LLMProcessor(llm_model)
        self.logger = logging.getLogger(__name__)
        
    def process_session(self, audio_path: str, output_dir: str = "output") -> Dict:
        """
        Process a complete therapy session from audio file to clinical notes
        
        Args:
            audio_path: Path to the audio file
            output_dir: Directory to save output files
            
        Returns:
            Dictionary containing all processing results
        """
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            # Step 1: Process audio
            console.print("📁 Starting session processing...", style="bold blue")
            transcript_data = self.audio_processor.process_audio(audio_path)
            
            # Step 2: Generate summaries and notes (if possible)
            llm_results = self.llm_processor.generate_session_summary(transcript_data)
            
            # Handle LLM processing gracefully - don't fail the entire process
            if "error" in llm_results:
                console.print("📝 Continuing with transcript-only output...", style="yellow")
                # Create basic results with just transcript
                results = {
                    **transcript_data,
                    "audio_file": audio_path,
                    "output_directory": output_dir,
                    "session_summary": "LLM processing not available - transcript generated successfully",
                    "soap_note": "SOAP note requires LLM processing (Ollama) - see setup instructions",
                    "llm_available": False,
                    "processing_notes": "Audio transcription completed. Install Ollama for AI-powered summaries."
                }
            else:
                # Full processing completed
                results = {
                    **transcript_data,
                    **llm_results,
                    "audio_file": audio_path,
                    "output_directory": output_dir,
                    "llm_available": True
                }
            
            # Step 4: Save outputs
            self._save_results(results, output_dir)
            
            console.print("✅ Session processing completed successfully!", style="bold green")
            return results
            
        except Exception as e:
            self.logger.error(f"Error processing session: {e}")
            console.print(f"❌ Error: {str(e)}", style="red")
            return {"error": str(e)}
    
    def _save_results(self, results: Dict, output_dir: str):
        """Save processing results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save transcript
        transcript_file = Path(output_dir) / f"transcript_{timestamp}.txt"
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write("THERAPY SESSION TRANSCRIPT\n")
            f.write("=" * 50 + "\n\n")
            f.write(results.get("transcript_formatted", results.get("transcript", "")))
        
        # Save session summary (with helpful message if LLM not available)
        summary_file = Path(output_dir) / f"summary_{timestamp}.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("SESSION SUMMARY\n")
            f.write("=" * 30 + "\n\n")
            
            summary_content = results.get("session_summary", "")
            if results.get("llm_available", True):  # Default to True for backward compatibility
                f.write(summary_content)
            else:
                f.write("AI-POWERED SUMMARY NOT AVAILABLE\n")
                f.write("-" * 35 + "\n\n")
                f.write("To get AI-powered session summaries:\n")
                f.write("1. Install Ollama: https://ollama.ai/\n")
                f.write("2. Run: ollama pull llama3.2\n")
                f.write("3. Process your audio again\n\n")
                f.write("TRANSCRIPT SUMMARY:\n")
                f.write(f"• Duration: {results.get('duration', 0):.1f} seconds\n")
                f.write(f"• Language: {results.get('language', 'unknown')}\n")
                f.write(f"• Diarization: {results.get('diarization_method', 'unknown')}\n")
                if 'segments' in results:
                    speakers = set(seg.get('speaker', 'Unknown') for seg in results['segments'])
                    f.write(f"• Speakers identified: {', '.join(sorted(speakers))}\n")
                f.write(f"• Processing notes: {results.get('processing_notes', '')}\n")
        
        # Save SOAP note (with helpful message if LLM not available)
        soap_file = Path(output_dir) / f"soap_note_{timestamp}.txt"
        with open(soap_file, 'w', encoding='utf-8') as f:
            f.write("SOAP NOTE\n")
            f.write("=" * 20 + "\n\n")
            
            soap_content = results.get("soap_note", "")
            if results.get("llm_available", True):
                f.write(soap_content)
            else:
                f.write("PROFESSIONAL SOAP NOTE GENERATION REQUIRES AI SETUP\n")
                f.write("-" * 50 + "\n\n")
                f.write("BASIC STRUCTURE (Complete after AI setup):\n\n")
                f.write("SUBJECTIVE:\n")
                f.write("(Client's reported experience - add after reviewing transcript)\n\n")
                f.write("OBJECTIVE:\n")
                f.write("(Observable behaviors - add after reviewing transcript)\n\n")
                f.write("ASSESSMENT:\n")  
                f.write("(Clinical impressions - requires AI analysis)\n\n")
                f.write("PLAN:\n")
                f.write("(Next steps - requires AI analysis)\n\n")
                f.write("TO GENERATE COMPLETE SOAP NOTE:\n")
                f.write("1. Install Ollama: https://ollama.ai/\n")
                f.write("2. Run: ollama pull llama3.2\n")
                f.write("3. Process your audio file again\n")
        
        # Save complete results as JSON
        json_file = Path(output_dir) / f"session_data_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            # Remove non-serializable items for JSON
            json_data = {k: v for k, v in results.items() if k not in ['segments']}
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        console.print(f"📄 Results saved to: {output_dir}", style="green")
        console.print(f"   - Transcript: {transcript_file.name}", style="dim")
        console.print(f"   - Summary: {summary_file.name}", style="dim")
        console.print(f"   - SOAP Note: {soap_file.name}", style="dim")
        console.print(f"   - Full Data: {json_file.name}", style="dim")

class EnhancedSessionProcessor(SessionProcessor):
    """Enhanced Session processor with advanced diarization and LLM enhancement"""
    
    def __init__(self, whisper_model: str = "base", llm_model: str = "llama3.2", 
                 use_advanced_diarization: bool = True, use_llm_enhancement: bool = True):
        """
        Initialize enhanced session processor
        
        Args:
            whisper_model: Whisper model size
            llm_model: Ollama model name
            use_advanced_diarization: Whether to use pyannote.audio
            use_llm_enhancement: Whether to use LLM for speaker role refinement
        """
        # Initialize base LLM processor
        self.llm_processor = LLMProcessor(llm_model)
        self.logger = logging.getLogger(__name__)
        
        # Use advanced audio processor instead of basic one
        self.audio_processor = AdvancedAudioProcessor(
            whisper_model, 
            use_pyannote=use_advanced_diarization,
            use_llm_enhancement=False  # We'll handle this separately
        )
        
        # Add LLM-enhanced diarization if requested
        self.use_llm_enhancement = use_llm_enhancement
        if use_llm_enhancement:
            self.llm_diarization = LLMEnhancedDiarization(self.llm_processor)
        else:
            self.llm_diarization = None
    
    def process_session(self, audio_path: str, output_dir: str = "output") -> Dict:
        """Enhanced session processing with advanced diarization"""
        
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            # Stage 1: Audio Processing with Advanced Diarization
            console.print("🎯 Stage 1: Audio processing and diarization", style="bold blue")
            transcript_data = self.audio_processor.process_audio(audio_path)
            
            # Stage 2: LLM-Enhanced Speaker Role Assignment (if enabled)
            if self.use_llm_enhancement and self.llm_diarization:
                console.print("🧠 Stage 2: LLM-enhanced speaker analysis", style="bold blue")
                enhanced_segments = self.llm_diarization.enhance_diarization(
                    transcript_data["segments"]
                )
                transcript_data["segments"] = enhanced_segments
                transcript_data["llm_enhanced"] = True
            else:
                transcript_data["llm_enhanced"] = False
            
            # Stage 3: LLM Clinical Analysis
            console.print("📝 Stage 3: Clinical analysis and documentation", style="bold blue")
            llm_results = self.llm_processor.generate_session_summary(transcript_data)
            
            if "error" in llm_results:
                return llm_results
            
            # Stage 4: Combine and Structure Results
            results = {
                **transcript_data,
                **llm_results,
                "audio_file": audio_path,
                "output_directory": output_dir,
                "processing_features": {
                    "advanced_diarization": self.audio_processor.use_pyannote,
                    "llm_enhancement": self.use_llm_enhancement,
                    "diarization_method": transcript_data.get("diarization_method", "simple")
                }
            }
            
            # Stage 5: Persist Results
            self._save_results(results, output_dir)
            
            console.print("✅ Enhanced session processing completed successfully!", style="bold green")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in enhanced processing: {e}")
            console.print(f"❌ Processing failed: {e}", style="red")
            return {"error": str(e)}

# Update main() to use enhanced processor by default
def main():
    """Main CLI interface - re-parses arguments for standalone use"""
    import argparse
    
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
    
    # Parse args and call the processing function
    args = parser.parse_args()
    return process_with_args(args)

def process_with_args(args):
    """Process audio with pre-parsed arguments - called from lightweight CLI"""
    
    # Handle lightweight commands first (no heavy imports needed)
    if args.version:
        console.print("Blackowiak LLM v1.0.0", style="bold blue")
        console.print("Advanced Therapy Session Processor", style="dim")
        return 0
    
    # Handle license activation
    if args.activate_license:
        license_manager = LicenseManager()
        success, message = license_manager.activate_license(args.activate_license)
        
        if success:
            console.print("✅ License activated successfully!", style="green")
            console.print(f"   {message}", style="dim")
        else:
            console.print("❌ License activation failed", style="red")
            console.print(f"   {message}", style="dim")
        
        return 0 if success else 1
    
    # Handle license info
    if args.license_info:
        license_manager = LicenseManager()
        is_licensed, message, license_info = license_manager.check_license()
        
        if is_licensed:
            console.print("✅ LICENSE INFORMATION", style="green")
            console.print(f"Email: {license_info['email']}")
            console.print(f"Type: {license_info['type']}")
            console.print(f"Expires: {license_info['expires']}")
            console.print(f"Usage count: {license_info['usage_count']}")
        else:
            console.print("❌ NO VALID LICENSE", style="red")
            console.print(f"   {message}", style="dim")
        
        return 0
    
    # Check license before processing
    license_manager = LicenseManager()
    is_licensed, license_message, license_info = license_manager.check_license()
    
    if not is_licensed:
        console.print("❌ LICENSE REQUIRED", style="red")
        console.print(f"   {license_message}", style="dim")
        console.print()
        console.print("To activate your license:", style="yellow")
        console.print("   python run.py --activate-license YOUR_LICENSE_CODE", style="dim")
        console.print()
        console.print("To purchase a license:", style="yellow")
        console.print("   Visit: https://blackowiak-llm.com/purchase", style="dim")
        return 1
    
    # Show license info
    console.print(f"✅ Licensed to: {license_info['email']}", style="green")
    console.print(f"   License type: {license_info['type']}", style="dim")
    console.print(f"   Usage: {license_info['usage_count']}", style="dim")
    console.print()
    
    # At this point, we know we need to process an audio file
    # So check if audio file was provided and exists
    if not args.audio_file:
        console.print("❌ Error: Audio file is required for processing", style="red")
        print("Usage: blackowiak-llm [options] <audio_file>")
        return 1
        
    if not os.path.exists(args.audio_file):
        console.print(f"❌ Error: Audio file not found: {args.audio_file}", style="red")
        return 1
    
    # NOW we can load heavy libraries since we know we need to process
    console.print("🔄 Initializing AI processing libraries...", style="yellow")
    whisper, torch, pyannote_pipeline, AudioSegment, pyannote_available = _lazy_import_audio_libs()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    # Initialize processor based on arguments
    if args.basic_mode:
        console.print("🔧 Using basic processing mode", style="dim")
        processor = SessionProcessor(args.whisper_model, args.llm_model)
    else:
        # Determine diarization method and LLM enhancement
        use_advanced_diarization = False
        use_llm_enhancement = not args.no_llm_enhancement
        
        if args.diarization == "advanced":
            if pyannote_available:
                use_advanced_diarization = True
                use_llm_enhancement = False  # Advanced mode: pyannote only, no LLM post-processing
                console.print("🎯 Using advanced speaker diarization (pyannote.audio only)", style="blue")
            else:
                console.print("⚠️  Advanced diarization requested but pyannote.audio not available.", style="yellow")
                console.print("    Install with: pip install -r requirements-advanced.txt", style="dim")
                console.print("    Falling back to simple diarization.", style="dim")
        elif args.diarization == "advanced-with-llm-post-processing":
            if pyannote_available:
                use_advanced_diarization = True
                use_llm_enhancement = not args.no_llm_enhancement  # Respect the --no-llm-enhancement flag
                console.print("🎯 Using advanced diarization + LLM post-processing", style="blue")
            else:
                console.print("⚠️  Advanced diarization requested but pyannote.audio not available.", style="yellow")
                console.print("    Install with: pip install -r requirements-advanced.txt", style="dim")
                console.print("    Falling back to simple diarization with LLM enhancement.", style="dim")
                use_llm_enhancement = not args.no_llm_enhancement
        elif args.diarization == "auto":
            use_advanced_diarization = pyannote_available
            if use_advanced_diarization:
                console.print("🎯 Auto-detected advanced diarization capabilities (pyannote only)", style="blue")
                use_llm_enhancement = False  # Auto mode uses advanced without LLM by default
            else:
                console.print("🔧 Using simple diarization (pyannote.audio not available)", style="dim")
                use_llm_enhancement = not args.no_llm_enhancement
        else:  # simple
            console.print("🔧 Using simple speaker diarization", style="dim")
            use_llm_enhancement = not args.no_llm_enhancement
        
        processor = EnhancedSessionProcessor(
            args.whisper_model, 
            args.llm_model,
            use_advanced_diarization=bool(use_advanced_diarization),
            use_llm_enhancement=use_llm_enhancement
        )
    
    # Process the session
    results = processor.process_session(args.audio_file, args.output)
    
    if "error" in results:
        return 1
    
    # Increment usage counter on successful processing
    license_manager.increment_usage()
    
    return 0
