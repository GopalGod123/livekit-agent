#!/usr/bin/env python3
"""
LiveKit Multi-Agent Demo
========================

This demo connects to LiveKit and provides a multi-agent AI system that can:
1. Handle sales queries 
2. Transfer to technical support
3. Transfer to billing support
4. Provide seamless agent handoffs

Usage:
    python livekit_demo.py

Requirements:
    - LiveKit server running
    - Valid LiveKit credentials
    - Audio input/output devices
"""

import asyncio
import os

# LiveKit Configuration
# 🔧 Update these with your LiveKit server details
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "wss://your-livekit-server.com")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "your-api-key")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "your-api-secret")

async def main():
    print("🚀 Starting LiveKit Multi-Agent Demo...")
    print("=" * 60)
    print("🤖 AI Agents Available:")
    print("   📊 SALES - Product demos, pricing, deals")
    print("   🔧 TECHNICAL - API, integrations, troubleshooting") 
    print("   💳 BILLING - Payments, subscriptions, invoices")
    print("   📞 AUTO-TRANSFER - Smart routing between agents")
    print("=" * 60)
    
    # Validate credentials
    if "your-" in LIVEKIT_URL or "your-" in LIVEKIT_API_KEY:
        print("❌ Please configure your LiveKit credentials!")
        print("   Set environment variables:")
        print("   - LIVEKIT_URL=wss://your-server.livekit.cloud")
        print("   - LIVEKIT_API_KEY=your-api-key") 
        print("   - LIVEKIT_API_SECRET=your-secret")
        print("\n💡 Or update the variables in this file directly")
        return
    
    try:
        from livekit_handler import MultiAgentLiveKitHandler
        
        # Initialize multi-agent handler
        handler = MultiAgentLiveKitHandler(
            url=LIVEKIT_URL,
            api_key=LIVEKIT_API_KEY,
            api_secret=LIVEKIT_API_SECRET
        )
        
        # Connect to LiveKit room
        room_name = "multi-agent-demo-room"
        print(f"🔗 Connecting to room: {room_name}")
        print("📱 Connect via LiveKit Playground or client app")
        print("🎙️ Start speaking to interact with AI agents")
        print("🔄 Agents will transfer calls automatically based on your queries")
        print("\nPress Ctrl+C to stop the demo")
        print("-" * 60)
        
        await handler.connect_and_handle_calls(room_name)
        
    except ImportError:
        print("❌ LiveKit not installed. Install with: pip install livekit")
        print("💡 Or run: python livekit_demo.py --test  (for local testing)")
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure your LiveKit server is running and credentials are correct")

def test_agents_locally():
    """Test the multi-agent system locally without LiveKit"""
    print("🧪 Testing Multi-Agent System Locally...")
    print("=" * 50)
    
    from agent_router import AgentRouter
    
    router = AgentRouter()
    
    # Test scenarios
    test_scenarios = [
        {
            "query": "Hi, I want to buy your premium plan. What's the pricing?",
            "expected_agent": "sales"
        },
        {
            "query": "I'm getting a 404 error when calling your API endpoint",
            "expected_agent": "technical" 
        },
        {
            "query": "My credit card was charged twice this month",
            "expected_agent": "billing"
        },
        {
            "query": "Can you show me a product demo?",
            "expected_agent": "sales"
        },
        {
            "query": "How do I integrate your SDK with Python?",
            "expected_agent": "technical"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📋 Test {i}: {scenario['query']}")
        print(f"🎯 Expected Agent: {scenario['expected_agent'].upper()}")
        
        response = router.route_query(scenario['query'])
        
        print(f"🤖 Current Agent: {router.current_agent.upper()}")
        print(f"💬 Response: {response[:100]}..." if len(response) > 100 else f"💬 Response: {response}")
        
        # Check if transfer happened correctly
        if router.current_agent == scenario['expected_agent']:
            print("✅ Correct agent routing!")
        else:
            print(f"⚠️  Expected {scenario['expected_agent']}, got {router.current_agent}")
        
        print("-" * 30)
    
    print(f"\n📊 Final Statistics:")
    print(f"   💬 Total interactions: {len(router.conversation_history)}")
    print(f"   🤖 Final agent: {router.current_agent.upper()}")
    print("✅ Local testing completed!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Run local testing
        test_agents_locally()
    else:
        # Run LiveKit demo
        asyncio.run(main()) 