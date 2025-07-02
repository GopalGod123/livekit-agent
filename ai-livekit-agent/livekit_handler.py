import asyncio
import logging
from livekit import api, rtc
from agent_router import AgentRouter
from whisper_handler import convert_audio_to_text
from tts_handler import speak_text
import tempfile
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiAgentLiveKitHandler:
    def __init__(self, url: str, api_key: str, api_secret: str):
        self.url = url
        self.api_key = api_key
        self.api_secret = api_secret
        self.router = AgentRouter()
        self.room = None
        
    async def connect_and_handle_calls(self, room_name: str = "multi-agent-demo"):
        """Connect to LiveKit room and handle real-time voice calls"""
        try:
            # Create room connection
            self.room = rtc.Room()
            
            # Set up event handlers
            self.room.on("participant_connected", self.on_participant_connected)
            self.room.on("track_published", self.on_track_published)
            self.room.on("track_subscribed", self.on_track_subscribed)
            
            # Connect to room
            token = await self.generate_token(room_name, "ai-agent")
            await self.room.connect(self.url, token)
            
            logger.info(f"🔗 Connected to LiveKit room: {room_name}")
            logger.info(f"🤖 Multi-agent system ready (Starting agent: {self.router.current_agent.upper()})")
            
            # Keep the connection alive
            while True:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"❌ LiveKit connection error: {e}")
            
    async def generate_token(self, room_name: str, participant_name: str):
        """Generate LiveKit access token"""
        token = api.AccessToken(self.api_key, self.api_secret)
        token.with_identity(participant_name)
        token.with_name(participant_name)
        token.with_grants(api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True,
        ))
        return token.to_jwt()
    
    def on_participant_connected(self, participant: rtc.RemoteParticipant):
        logger.info(f"👤 User connected: {participant.identity}")
        
    def on_track_published(self, publication: rtc.RemoteTrackPublication, participant: rtc.RemoteParticipant):
        logger.info(f"📺 Track published: {publication.kind} from {participant.identity}")
        
    async def on_track_subscribed(self, track: rtc.Track, publication: rtc.RemoteTrackPublication, participant: rtc.RemoteParticipant):
        """Handle incoming audio from user"""
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            logger.info(f"🎧 Audio track subscribed from {participant.identity}")
            
            # Process audio stream
            audio_stream = rtc.AudioStream(track)
            async for frame in audio_stream:
                await self.process_audio_frame(frame, participant)
                
    async def process_audio_frame(self, frame: rtc.AudioFrame, participant: rtc.RemoteParticipant):
        """Process incoming audio and generate AI response"""
        try:
            # Save audio frame to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                # Convert frame to audio file (simplified - you'd need proper audio processing)
                temp_file.write(frame.data)
                temp_file_path = temp_file.name
            
            # Convert speech to text
            user_text = convert_audio_to_text(temp_file_path)
            logger.info(f"🧍 User said: {user_text}")
            
            if user_text.strip():
                # Route through multi-agent system
                response = self.router.route_query(user_text)
                logger.info(f"🤖 Agent ({self.router.current_agent.upper()}) response: {response}")
                
                # Convert response to speech
                response_audio_path = speak_text(response, f"response_{participant.identity}.mp3")
                
                # Send audio response back to user
                await self.send_audio_response(response_audio_path)
                
                # Clean up temp files
                os.unlink(temp_file_path)
                os.unlink(response_audio_path)
                
        except Exception as e:
            logger.error(f"❌ Error processing audio: {e}")
            
    async def send_audio_response(self, audio_file_path: str):
        """Send AI response audio back to room"""
        try:
            # Create audio track from file
            audio_source = rtc.AudioSource(sample_rate=44100, num_channels=1)
            track = rtc.LocalAudioTrack.create_audio_track("ai-response", audio_source)
            
            # Publish track
            await self.room.local_participant.publish_track(track)
            logger.info("🔊 AI response sent to room")
            
        except Exception as e:
            logger.error(f"❌ Error sending audio response: {e}")

# Legacy function for backward compatibility
def connect_to_livekit_and_stream(callback):
    """Legacy function - now shows how to use multi-agent system"""
    print("🚀 Connecting to LiveKit Multi-Agent System...")
    print("💡 To test with real LiveKit:")
    print("   1. Set up LiveKit server credentials")
    print("   2. Use: python livekit_demo.py")
    print("   3. Connect via LiveKit Playground")
    print("-" * 50)
    
    # For demo purposes, simulate the multi-agent system
    router = AgentRouter()
    
    # Simulate some test queries
    test_queries = [
        "I want to buy your product, what's the price?",
        "I'm having API integration issues",
        "Can you help me with my billing?",
        "What's your refund policy?"
    ]
    
    for query in test_queries:
        print(f"\n🎧 Simulating query: {query}")
        response = router.route_query(query)
        print(f"🤖 Response: {response}")
        
    print(f"\n📊 Final agent: {router.current_agent.upper()}")
    print("🔊 Multi-agent demo completed!")
