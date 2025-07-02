import sounddevice as sd
import soundfile as sf
import os

def play_audio(file_path):
    """Play audio file using sounddevice"""
    print("🔊 Playing:", file_path)
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"❌ Audio file not found: {file_path}")
            return
        
        # Read audio file
        data, samplerate = sf.read(file_path)
        
        # Play audio
        sd.play(data, samplerate)
        sd.wait()  # Wait until audio finishes playing
        print("✅ Audio playback completed")
        
    except Exception as e:
        print(f"❌ Error playing audio: {e}")
