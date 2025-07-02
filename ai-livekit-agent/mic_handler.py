import sounddevice as sd
import soundfile as sf

def record_audio(file_name="user_input.wav", duration=10, samplerate=44100):
    print("🎙️ Recording...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    sf.write(file_name, audio, samplerate)
    print("✅ Saved:", file_name)
    return file_name
