# 🤖 Multi-Agent AI Voice System

A sophisticated AI voice agent system that automatically transfers calls between specialized agents based on user queries. Perfect for customer service, sales, and technical support scenarios.

## 🌟 Features

### 🔄 **Smart Agent Routing**
- **Sales Agent**: Handles pricing, demos, product information
- **Technical Agent**: API support, integrations, troubleshooting  
- **Billing Agent**: Payments, subscriptions, invoices
- **Auto-Transfer**: Seamless handoffs between agents

### 🎙️ **Voice Capabilities**
- Real-time speech recognition (Whisper)
- Natural language processing (Together AI)
- Text-to-speech responses (Google TTS)
- Audio playback system

### 📞 **LiveKit Integration**
- Real-time voice calls via LiveKit
- WebRTC support for browser clients
- Production-ready voice agents
- LiveKit Playground compatible

## 🚀 Quick Start

### 1. Installation

```bash
# Clone and setup
cd ai-livekit-agent
pip install -r requirements.txt
```

### 2. Test Locally (No LiveKit needed)

```bash
# Test the multi-agent system locally
python livekit_demo.py --test
```

### 3. Run Voice Agent Locally

```bash
# Run with microphone input
python main.py
```

### 4. Test with LiveKit Playground

```bash
# Setup LiveKit credentials first
export LIVEKIT_URL="wss://your-server.livekit.cloud"
export LIVEKIT_API_KEY="your-api-key"
export LIVEKIT_API_SECRET="your-secret"

# Run LiveKit demo
python livekit_demo.py
```

## 🧪 Testing Scenarios

### Local Testing Examples

Try these queries to see agent transfers:

```bash
python livekit_demo.py --test
```

**Sales Queries** (stays with sales agent):
- "What's your pricing?"
- "I want to buy your product"
- "Can you show me a demo?"

**Technical Queries** (transfers to technical):
- "I'm getting API errors"
- "How do I integrate your SDK?"
- "My code isn't working"

**Billing Queries** (transfers to billing):
- "I was charged twice"
- "Cancel my subscription"
- "Need an invoice"

## 🔧 LiveKit Setup

### Option 1: LiveKit Cloud

1. Sign up at [LiveKit Cloud](https://cloud.livekit.io)
2. Create a project
3. Get your credentials:
   ```bash
   export LIVEKIT_URL="wss://your-project.livekit.cloud"
   export LIVEKIT_API_KEY="your-api-key"
   export LIVEKIT_API_SECRET="your-secret"
   ```

### Option 2: Self-hosted LiveKit

```bash
# Run LiveKit server locally
docker run --rm -p 7880:7880 -p 7881:7881 \
  livekit/livekit-server --dev
```

### Testing with LiveKit Playground

1. Start the agent:
   ```bash
   python livekit_demo.py
   ```

2. Open [LiveKit Playground](https://playground.livekit.io)

3. Connect to room: `multi-agent-demo-room`

4. Start speaking! The AI will:
   - Listen to your voice
   - Route to appropriate agent
   - Respond with voice
   - Transfer between agents automatically

## 🏗️ Architecture

```
User Voice Input
      ↓
   Whisper STT
      ↓
  Agent Router
      ↓
┌─────────────────┐
│  Sales Agent    │ ←→ Technical Agent
│  - Pricing      │     - API Support
│  - Demos        │     - Integration
│  - Features     │     - Debugging
└─────────────────┘
      ↓
┌─────────────────┐
│  Billing Agent  │
│  - Payments     │
│  - Subscriptions│
│  - Invoices     │
└─────────────────┘
      ↓
   Google TTS
      ↓
  Audio Playback
```

## 📁 File Structure

```
ai-livekit-agent/
├── main.py              # Local voice agent
├── agent_router.py      # Multi-agent system
├── livekit_handler.py   # LiveKit integration
├── livekit_demo.py      # LiveKit testing
├── whisper_handler.py   # Speech recognition
├── together_handler.py  # AI responses
├── tts_handler.py       # Text-to-speech
├── audio_player.py      # Audio playback
└── mic_handler.py       # Microphone input
```

## 🛠️ Configuration

### API Keys Required

```bash
# Together AI (in together_handler.py)
TOGETHER_API_KEY="your-together-ai-key"

# LiveKit (environment variables)
LIVEKIT_URL="wss://your-server.livekit.cloud"
LIVEKIT_API_KEY="your-api-key"
LIVEKIT_API_SECRET="your-secret"
```

### Agent Customization

Edit `agent_router.py` to customize:
- Agent specializations
- Transfer logic keywords
- Response templates
- New agent types

## 🎯 Use Cases

### Customer Service
- **Level 1**: General inquiries → **Sales Agent**
- **Level 2**: Technical issues → **Technical Agent**  
- **Level 3**: Billing problems → **Billing Agent**

### Sales Automation
- **Qualification**: Sales agent qualifies leads
- **Technical Demo**: Transfers to technical for deep dive
- **Closing**: Back to sales for contract discussion

### Support Escalation
- **Tier 1**: Basic support questions
- **Tier 2**: Technical troubleshooting
- **Tier 3**: Billing and account issues

## 🔍 Monitoring & Logs

The system provides detailed logging:

```python
🤖 Current Agent: SALES
🔄 Transferring call from sales to technical
🧍 User: I'm getting API errors
🤖 Agent (TECHNICAL) response: Let me help you with that API issue...
```

## 🚀 Production Deployment

### Scaling Options

1. **Single Agent**: `python main.py`
2. **LiveKit Integration**: `python livekit_demo.py`
3. **Multiple Rooms**: Deploy multiple agent instances
4. **Load Balancing**: Use LiveKit's built-in load balancing

### Performance Tips

- Use GPU for Whisper inference
- Cache TTS responses
- Implement conversation memory
- Add agent analytics

## 🤝 Contributing

The multi-agent system is modular and extensible:

1. **Add New Agents**: Inherit from `BaseAgent`
2. **Custom Routing**: Modify `should_transfer()` logic
3. **New Features**: Add to agent specializations
4. **Integration**: Connect to your existing systems

## 📞 Real-World Testing

### With LiveKit Playground

1. **Start Agent**: `python livekit_demo.py`
2. **Open Playground**: https://playground.livekit.io
3. **Join Room**: `multi-agent-demo-room`
4. **Test Scenarios**:
   - "I want to buy your product" → Sales
   - "API integration help" → Technical
   - "Billing question" → Billing

### Production Ready

- ✅ Real-time voice processing
- ✅ Multi-agent routing
- ✅ WebRTC compatibility
- ✅ Scalable architecture
- ✅ Error handling
- ✅ Logging & monitoring

---

**Ready to test?** Start with `python livekit_demo.py --test` to see the magic! 🎊
