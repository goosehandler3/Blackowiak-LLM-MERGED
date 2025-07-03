# Creating Demo Audio for Testing

Since we can't include actual therapy session recordings, here are several ways you can create demo audio files for testing:

## Option 1: Text-to-Speech (Recommended)

### Using macOS built-in TTS:
```bash
# Create therapist audio
say -v Alex -o therapist.wav "Good morning, thank you for coming in today. How are you feeling?"

# Create client audio  
say -v Samantha -o client.wav "I'm doing okay, I guess. It's been a rough week though."

# Combine using audio editing software or ffmpeg
```

### Using Python TTS libraries:
```python
import pyttsx3
import wave

# This would require: pip install pyttsx3
engine = pyttsx3.init()
engine.save_to_file("Your text here", "output.wav")
engine.runAndWait()
```

## Option 2: Online TTS Services

1. **Google Cloud Text-to-Speech**: High quality, requires API key
2. **Amazon Polly**: Very natural voices, requires AWS account
3. **ElevenLabs**: Extremely realistic voices, free tier available

## Option 3: Record Your Own

1. Use QuickTime Player (Mac) or Voice Recorder (Windows)
2. Record yourself reading the demo transcript
3. Use different voices/tones for therapist vs client
4. Save as WAV or MP3 format

## Option 4: Use Existing Audio

Any audio file with two speakers works for testing:
- Podcast episodes
- Interview recordings  
- Meeting recordings
- YouTube videos (downloaded as audio)

## Testing the System

Once you have audio:
```bash
python run.py path/to/your/audio.wav
```

The system will:
1. Transcribe the audio
2. Identify speakers (basic algorithm)
3. Generate session summary
4. Create SOAP note

## Notes

- Longer audio files (30+ minutes) provide better testing
- Clear audio with minimal background noise works best
- The speaker diarization is basic - it alternates speakers based on pauses
- For production use, you'd want more sophisticated speaker identification
