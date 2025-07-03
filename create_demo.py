#!/usr/bin/env python3
"""
Demo Audio Generator for Blackowiak LLM Testing

This script creates a synthetic audio file simulating a therapy session
for testing purposes. Uses text-to-speech to create a realistic demo.
"""

import sys
import os
from pathlib import Path

def create_demo_transcript():
    """Create a realistic therapy session transcript for demo purposes"""
    return """
[0.0s] Therapist: Good morning, thank you for coming in today. How are you feeling?

[3.2s] Client: I'm doing okay, I guess. It's been a rough week though.

[7.1s] Therapist: I'm sorry to hear that. What's been making it particularly challenging?

[11.5s] Client: Work has been really stressful. My manager keeps piling on more projects, and I feel like I can't keep up. I've been losing sleep over it.

[18.9s] Therapist: That sounds overwhelming. When you say you're losing sleep, can you tell me more about that?

[23.4s] Client: I lie awake at night thinking about all the things I need to do. My mind just races. I probably get about four or five hours of sleep on a good night.

[31.2s] Therapist: Sleep is so important for managing stress and emotions. Have you noticed how the lack of sleep affects you during the day?

[37.8s] Client: Oh definitely. I'm irritable, I can't concentrate, and I feel like I'm just going through the motions. Yesterday I snapped at my partner over something really small.

[46.1s] Therapist: It sounds like you're recognizing the connections between your sleep, stress, and relationships. That's actually really insightful. How did your partner respond when you snapped?

[54.3s] Client: They were understanding, which made me feel even worse. They said I seemed stressed and asked if I wanted to talk about it. But I just shut down.

[62.7s] Therapist: It can be hard to open up when we're feeling overwhelmed. What do you think made it difficult to share with your partner in that moment?

[69.9s] Client: I guess I was embarrassed. I feel like I should be able to handle work stress better. I don't want to be a burden.

[77.4s] Therapist: That's a common feeling, but let's explore that word 'burden.' What makes you feel like sharing your struggles would be burdensome?

[84.8s] Client: I don't know. I guess I've always been the one who has it together. People come to me for advice. It feels weird to be the one who needs support.

[93.2s] Therapist: That's a significant insight. It sounds like you've taken on a role of being the strong one, the helper. But everyone needs support sometimes. What do you think would happen if you let your partner support you?

[103.5s] Client: I... I'm not sure. Maybe they'd see me differently? Like I'm not as capable as they thought?

[109.8s] Therapist: Those are understandable fears. In healthy relationships, vulnerability often brings people closer together rather than pushing them apart. Have you seen your partner be vulnerable with you?

[119.2s] Client: Yeah, definitely. When they lost their job last year, they were really scared and upset. I was there for them.

[126.4s] Therapist: And how did that affect your relationship? Did you think less of them for being vulnerable?

[131.9s] Client: No, not at all. If anything, I felt closer to them. I was proud that they trusted me enough to share their fears.

[139.7s] Therapist: That's beautiful. So you were able to be there for them without judgment, and it actually strengthened your bond. What do you think about applying that same compassion to yourself?

[148.8s] Client: I... I never thought about it that way. I guess I have a double standard.

[154.1s] Therapist: Many of us do. We're often much kinder to others than we are to ourselves. For this week, I'd like you to try one small step toward self-compassion. What's one thing you could do?

[164.5s] Client: Maybe I could try talking to my partner about work. Just once, to see how it feels.

[170.2s] Therapist: That sounds like a wonderful and brave first step. How are you feeling about our conversation today?

[176.3s] Client: Good, actually. Lighter somehow. I feel like I have a direction now.

[181.8s] Therapist: I'm glad to hear that. We'll continue exploring these patterns next week. Take care of yourself, and remember - you deserve the same kindness you give others.

[190.5s] Client: Thank you. I'll try to remember that.
""".strip()

def save_demo_transcript():
    """Save the demo transcript to a file"""
    transcript = create_demo_transcript()
    
    # Create example_data directory if it doesn't exist
    example_dir = Path("example_data")
    example_dir.mkdir(exist_ok=True)
    
    # Save transcript
    transcript_file = example_dir / "demo_session_transcript.txt"
    with open(transcript_file, 'w', encoding='utf-8') as f:
        f.write("DEMO THERAPY SESSION TRANSCRIPT\n")
        f.write("=" * 50 + "\n\n")
        f.write("NOTE: This is a fictional therapy session created for testing purposes.\n")
        f.write("It demonstrates the expected input/output format for the Blackowiak LLM system.\n\n")
        f.write(transcript)
    
    print(f"✅ Demo transcript saved to: {transcript_file}")
    return transcript_file

def create_demo_audio_instructions():
    """Create instructions for generating demo audio"""
    instructions = """# Creating Demo Audio for Testing

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
"""
    
    instructions_file = Path("example_data") / "CREATE_DEMO_AUDIO.md"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✅ Demo audio instructions saved to: {instructions_file}")
    return instructions_file

def main():
    """Main function to create demo materials"""
    print("🎬 Creating Demo Materials for Blackowiak LLM")
    print("=" * 50)
    
    # Create transcript
    transcript_file = save_demo_transcript()
    
    # Create audio instructions
    instructions_file = create_demo_audio_instructions()
    
    print("\n✅ Demo materials created successfully!")
    print("\nWhat was created:")
    print(f"- Demo transcript: {transcript_file}")
    print(f"- Audio creation guide: {instructions_file}")
    
    print("\nNext steps:")
    print("1. Follow the instructions in CREATE_DEMO_AUDIO.md to create test audio")
    print("2. Run: python test_installation.py")
    print("3. Run: python run.py path/to/your/audio.wav")
    
    return 0

if __name__ == "__main__":
    exit(main())
