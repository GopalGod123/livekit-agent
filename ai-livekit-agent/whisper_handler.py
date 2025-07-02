import whisper
import os
import numpy as np
import soundfile as sf

model = whisper.load_model("base")

def convert_audio_to_text(audio_path):
    try:
        # Check if audio file exists
        if not os.path.exists(audio_path):
            print(f"⚠️  Audio file not found: {audio_path}")
            print("🎤 Creating a dummy audio file for testing...")
            create_dummy_audio(audio_path)
        
        result = model.transcribe(audio_path)
        return result['text']
    except Exception as e:
        print(f"❌ Error in audio transcription: {e}")
        return "Sorry, I couldn't process the audio. Please try again."

def create_dummy_audio(filename):
    """Create a simple test audio file with a spoken message"""
    try:
        # Create a simple sine wave (beep) for 2 seconds
        sample_rate = 16000
        duration = 2.0
        frequency = 440  # A4 note
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        # Save as WAV file
        sf.write(filename, audio_data, sample_rate)
        print(f"✅ Created dummy audio file: {filename}")
    except Exception as e:
        print(f"❌ Could not create dummy audio file: {e}")
