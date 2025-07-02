import utils.session
from mic_handler import record_audio
from whisper_handler import convert_audio_to_text
from agent_router import AgentRouter
from tts_handler import speak_text
from audio_player import play_audio

if __name__ == "__main__":
    print("🧠 Multi-Agent AI System Started... (Press Ctrl+C to stop)")
    print("📞 Starting with SALES agent - can transfer to Technical/Billing agents as needed")
    print("-" * 60)
    
    # Initialize the agent router
    router = AgentRouter()
    
    try:
        while True:
            print(f"\n🎙️ Recording (Current Agent: {router.current_agent.upper()})...")
            audio_file = record_audio()
            user_text = convert_audio_to_text(audio_file)
            print("🧍 You:", user_text)

            if user_text.strip() == "":
                print("❌ No speech detected, please try again.")
                continue

            # Route query through agent system
            response = router.route_query(user_text)
            print("🤖 AI:", response)

            # Convert response to speech and play
            output_audio = speak_text(response)
            play_audio(output_audio)

    except KeyboardInterrupt:
        print("\n👋 Multi-Agent system stopped.")
        print(f"📊 Final agent: {router.current_agent.upper()}")
        print(f"💬 Total interactions: {len(router.conversation_history)}")
