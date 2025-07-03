# 🧠 BLACKOWIAK LLM - QUICK START CARD

**AI-Powered Therapy Documentation | Completely Private & Offline**

---

## ⚡ **SETUP (One Time - 5 Minutes)**

### **1. Install Dependencies**
```bash
# macOS
brew install ffmpeg
# Download Ollama from: https://ollama.ai/

# Windows  
# Download ffmpeg from: https://ffmpeg.org/
# Download Ollama from: https://ollama.ai/

# Linux
sudo apt install ffmpeg
curl -fsSL https://ollama.ai/install.sh | sh
```

### **2. Install AI Model**
```bash
ollama pull llama3.2
```

### **3. Activate License**
```bash
python run.py --activate-license YOUR_LICENSE_CODE
```

---

## 🎵 **DAILY USE (30 seconds)**

### **Basic Processing**
```bash
python run.py session_audio.wav
```

### **High Quality**
```bash
python run.py --whisper-model large --diarization advanced session_audio.wav
```

### **Custom Output**
```bash
python run.py --output results/ session_audio.wav
```

---

## 📁 **WHAT YOU GET**

✅ **Complete Transcript** with speaker labels  
✅ **Clinical Summary** of key themes  
✅ **SOAP Note** ready for documentation  
✅ **JSON Data** for EMR integration  

---

## 🔒 **100% PRIVATE**
- ✅ No internet required (after setup)
- ✅ No cloud uploads ever
- ✅ All processing on your computer
- ✅ You control all data

---

## 🆘 **NEED HELP?**

**📧 support@blackowiak-llm.com**  
**🌐 blackowiak-llm.com/support**

```bash
# Check license
python run.py --license-info

# Get help
python run.py --help

# Test with example
python run.py example_data/demo_audio.wav
```

---

**💡 TIP**: Start with small test files to get familiar, then process your real sessions!
