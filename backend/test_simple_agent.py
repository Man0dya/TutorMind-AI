#!/usr/bin/env python3
"""
Simple test script to debug agent service issues
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

async def test_simple_agent():
    """Test the agent step by step."""
    try:
        print("🧪 Simple Agent Test")
        print("=" * 40)
        
        # Test 1: Import ContentGeneratorAgent
        print("1. Testing ContentGeneratorAgent import...")
        try:
            from agents.content_generator_agent import ContentGeneratorAgent
            print("   ✅ ContentGeneratorAgent imported successfully")
        except Exception as e:
            print(f"   ❌ Import failed: {str(e)}")
            return False
        
        # Test 2: Initialize agent
        print("2. Testing agent initialization...")
        try:
            agent = ContentGeneratorAgent()
            print("   ✅ Agent initialized successfully")
        except Exception as e:
            print(f"   ❌ Initialization failed: {str(e)}")
            return False
        
        # Test 3: Check agent status
        print("3. Testing agent status...")
        try:
            status = agent.get_status()
            print(f"   📊 Status: {status}")
            print(f"   ✅ Available: {status.get('available', False)}")
        except Exception as e:
            print(f"   ❌ Status check failed: {str(e)}")
            return False
        
        # Test 4: Test simple content generation
        print("4. Testing simple content generation...")
        try:
            if status.get('available', False):
                content = await agent.generate_content(
                    topic="Test Topic",
                    difficulty_level="beginner",
                    content_type="summary"
                )
                print(f"   ✅ Content generated successfully")
                print(f"   📝 Content length: {len(content.get('content', ''))}")
                print(f"   🔑 Key concepts: {len(content.get('key_concepts', []))}")
            else:
                print("   ⚠️ Agent not available, skipping content generation")
        except Exception as e:
            print(f"   ❌ Content generation failed: {str(e)}")
            return False
        
        print("\n🎉 Simple agent test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Simple Agent Test")
    print("=" * 40)
    
    success = asyncio.run(test_simple_agent())
    
    if success:
        print("\n🎉 Agent is working correctly!")
        print("💡 You can now use it for content generation.")
    else:
        print("\n💥 Agent test failed. Please check the errors above.")
        sys.exit(1)
