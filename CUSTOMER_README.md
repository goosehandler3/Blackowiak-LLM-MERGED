# Blackowiak LLM - Professional Edition

**AI-Powered Therapy Session Processor**  
*Process audio sessions into professional clinical documentation - completely offline*

---

## 🚀 **QUICK START (5 Minutes)**

### **1. Install Blackowiak LLM**
1. Download the macOS package (Blackowiak-LLM-macOS)
2. Copy the entire folder to your Applications directory
3. Open Terminal and navigate to the application folder

### **2. Run the Installer**
```bash
cd /Applications/Blackowiak-LLM-macOS/
python installer.py
```
*The installer will check dependencies and guide you through setup*

### **3. Activate Your License**
```bash
./blackowiak-llm --activate-license YOUR_LICENSE_CODE
```
*Your license code was sent to your email after purchase*

### **4. Process Your First Session**
```bash
./blackowiak-llm your_audio_file.wav
```

**That's it!** Your processed session will appear in the `output/` folder with:
- ✅ Complete transcript with speaker identification
- ✅ Professional session summary
- ✅ SOAP note ready for your records

---

## 💻 **SYSTEM REQUIREMENTS**

### **Minimum Requirements**
- **Operating System**: macOS 10.15+ (Catalina or newer)
- **RAM**: 4GB available (8GB recommended for large files)
- **Storage**: 8GB free space (for AI models and processing cache)
- **Internet**: Required for first-time setup only

### **Required Dependencies**
These are installed separately as they require user setup:

1. **Ollama** (for AI summaries)
   - Download: https://ollama.ai/
   - Install model: `ollama pull llama3.2`
   - Runs automatically after installation

2. **FFmpeg** (for audio processing)
   - Install: `brew install ffmpeg`
   - Handles all audio formats

3. **Hugging Face Setup** (optional, for advanced speaker identification)
   - Create account: https://huggingface.co/join
   - Get access token: https://huggingface.co/settings/tokens
   - Accept model license: https://huggingface.co/pyannote/speaker-diarization-3.1
   - Login: `huggingface-cli login`

---

## 🎯 **WHAT WORKS WITHOUT SETUP**

Even without all dependencies, you still get:
- ✅ **Basic audio transcription** (built-in)
- ✅ **Simple speaker detection** (built-in)
- ✅ **Text output** (built-in)

**With Full Setup:**
- ✅ **AI-powered session summaries** (requires Ollama)
- ✅ **Advanced speaker identification** (requires Hugging Face)
- ✅ **All audio formats** (requires FFmpeg)

---

## 🎵 **SUPPORTED AUDIO FORMATS**

✅ **Audio Files**: WAV, MP3, M4A, FLAC, OGG  
✅ **Recording Quality**: Any sample rate, mono or stereo  
✅ **Session Length**: Up to 3 hours per file  
✅ **File Size**: Up to 2GB per audio file  

---

## 📋 **WHAT YOU GET**

### **Output Files** (Generated for each session)
```
output/
├── transcript_20250628_143022.txt    # Complete transcript with speakers
├── summary_20250628_143022.txt       # Clinical session summary  
├── soap_note_20250628_143022.txt     # Professional SOAP note
└── session_data_20250628_143022.json # Complete data for integration
```

### **Clinical Templates Included**
- **SOAP Notes**: Subjective, Objective, Assessment, Plan
- **BIRP Notes**: Behavior, Intervention, Response, Plan
- **DAP Notes**: Description, Assessment, Plan
- **Session Summaries**: Therapeutic insights and progress
- **Custom Templates**: Modify or create your own formats

---

## 🔒 **PRIVACY & SECURITY**

### **100% Local Processing**
- ✅ **No cloud uploads**: All audio stays on your computer
- ✅ **No internet required**: After initial setup, works completely offline
- ✅ **HIPAA compliant**: When used according to guidelines
- ✅ **Your data, your control**: You own and manage all generated content

### **License Protection**
- 🔐 **Secure activation**: License tied to your specific computer
- 📊 **Usage tracking**: Monitor your session processing history
- 🔄 **Annual renewal**: Ensures continued updates and support

---

## ⚙️ **ADVANCED OPTIONS**

### **Speaker Diarization Modes**
```bash
# Basic speaker detection (faster)
./blackowiak-llm --diarization simple session.wav

# Advanced AI speaker identification (recommended)
./blackowiak-llm --diarization advanced session.wav

# Advanced + role assignment (therapist/client)
./blackowiak-llm --diarization advanced-with-llm-post-processing session.wav
```

### **Accuracy vs Speed Options**
```bash
# Fastest processing (good accuracy)
./blackowiak-llm --whisper-model tiny session.wav

# Balanced performance (recommended)
./blackowiak-llm --whisper-model base session.wav

# Highest accuracy (slower)
./blackowiak-llm --whisper-model large session.wav
```

### **Custom Output Location**
```bash
# Save to specific folder
./blackowiak-llm --output /path/to/results session.wav

# Process with different AI models
./blackowiak-llm --llm-model llama3.2 session.wav
```

---

## 🆘 **GETTING HELP**

### **Installation Issues**
1. **Run the installer again** - it will check and fix missing dependencies
2. **Check system requirements** - ensure you meet minimum specs
3. **Contact support** - we're here to help!

### **Processing Issues**
```bash
# Check your license status
./blackowiak-llm --license-info

# Get detailed help
./blackowiak-llm --help

# Test with example audio
./blackowiak-llm example_data/demo_calendar.ics
```

### **Common Setup Issues**

**"FFmpeg not found"**
```bash
# Install FFmpeg on macOS
brew install ffmpeg
```

**"Ollama not available"**
```bash
# Install and setup Ollama
# Download from: https://ollama.ai/
ollama pull llama3.2
```

**"Advanced diarization failed"**
```bash
# Setup Hugging Face authentication
huggingface-cli login
# Enter your HF token when prompted
```

**"License activation failed"**
- Check your internet connection
- Verify you're using the correct license code
- Contact support if issues persist

### **Support Channels**
- 📧 **Email**: support@blackowiak-llm.com
- 🌐 **Website**: https://blackowiak-llm.com/support
- 📚 **Documentation**: Full guides in your installation folder
- 💬 **Priority Support**: Available for Professional license holders

---

## 🎯 **TYPICAL WORKFLOW**

### **For Individual Therapists**
1. **Record session** (with client consent)
2. **Save audio file** to your computer
3. **Process with Blackowiak LLM**: `python run.py session.wav`
4. **Review and edit** generated notes as needed
5. **Save to client file** or EMR system

### **For Group Practices**
1. **Standardized processing** across all therapists
2. **Consistent documentation** quality and format
3. **Time savings** of 2+ hours per therapist per day
4. **Improved compliance** with professional standards

---

## 📈 **PERFORMANCE EXPECTATIONS**

### **Processing Times** (varies by system)
- **15-minute session**: ~3-5 minutes to process
- **60-minute session**: ~8-12 minutes to process
- **Factors**: Audio quality, speaker separation, chosen accuracy level

### **Accuracy Rates**
- **Transcription**: 90-95% accuracy with clear audio
- **Speaker identification**: 85-95% accuracy with distinct voices
- **Clinical content**: Professional-grade summaries and notes

---

## 🔄 **UPDATES & MAINTENANCE**

### **Automatic Features**
- ✅ **License validation**: Checked automatically
- ✅ **Usage tracking**: Sessions counted automatically
- ✅ **Error reporting**: Clear messages for any issues

### **Manual Updates**
- 📥 **Software updates**: Download new versions from your account
- 🔄 **AI model updates**: Ollama handles model management
- 📚 **Template updates**: New clinical formats released periodically

---

## 💡 **TIPS FOR BEST RESULTS**

### **Audio Recording**
- 🎤 **Use good microphones** for clearer transcripts
- 🔇 **Minimize background noise** when possible
- 🗣️ **Speak clearly** and avoid talking over each other
- ⏱️ **Keep files under 2 hours** for optimal processing

### **Clinical Documentation**
- ✏️ **Review all generated content** before finalizing
- 🔍 **Edit for accuracy** - AI assists but doesn't replace professional judgment
- 📝 **Customize templates** to match your documentation style
- 🔐 **Follow HIPAA guidelines** for all audio and text handling

---

## 📞 **NEED HELP?**

**We're here to ensure your success with Blackowiak LLM!**

### **Quick Support**
- 📧 Email: support@blackowiak-llm.com
- 📞 Priority Phone: Available for Professional license holders
- 💬 Live Chat: Available during business hours

### **Self-Service Resources**
- 📹 **Video Tutorials**: Step-by-step guides for common tasks
- 📖 **User Manual**: Complete documentation in your installation
- 🔧 **Troubleshooting Guide**: Solutions for common issues
- 💬 **User Community**: Connect with other therapists using the tool

---

**🎉 Welcome to the future of therapy documentation!**

*Save hours every week while improving the quality and consistency of your clinical notes.*

---

**Blackowiak LLM Professional Edition**  
*Created by Andrew Blackowiak, MSW*  
*Athens, GA · Therapist · Technologist · Millennial Futurist*

*Version 1.0 | Licensed Software | © 2025*
