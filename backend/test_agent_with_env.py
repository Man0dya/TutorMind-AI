#!/usr/bin/env python3
"""
Test script that properly loads environment variables before testing the agent
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

async def test_agent_with_env():
    """Test the agent with proper environment variable loading."""
    try:
        print("🧪 Agent Test with Environment Variables")
        print("=" * 50)
        
        # Check environment variables
        print("1. Checking environment variables...")
        gemini_key = os.getenv("GEMINI_API_KEY")
        mongodb_uri = os.getenv("MONGODB_URI")
        
        if gemini_key:
            print(f"   ✅ GEMINI_API_KEY found: {gemini_key[:10]}...")
        else:
            print("   ❌ GEMINI_API_KEY not found")
            return False
            
        if mongodb_uri:
            print(f"   ✅ MONGODB_URI found: {mongodb_uri[:30]}...")
        else:
            print("   ❌ MONGODB_URI not found")
            return False
        
        # Test 2: Import and initialize agent
        print("2. Testing agent initialization...")
        try:
            from agents.content_generator_agent import ContentGeneratorAgent
            agent = ContentGeneratorAgent()
            print("   ✅ Agent initialized successfully")
        except Exception as e:
            print(f"   ❌ Agent initialization failed: {str(e)}")
            return False
        
        # Test 3: Check agent status
        print("3. Testing agent status...")
        try:
            status = agent.get_status()
            print(f"   📊 Status: {status}")
            
            if status.get('available', False):
                print("   ✅ Agent is available and ready!")
            else:
                print("   ❌ Agent is not available")
                print(f"   🔍 Details: {status}")
                return False
                
        except Exception as e:
            print(f"   ❌ Status check failed: {str(e)}")
            return False
        
        # Test 4: Test content generation
        print("4. Testing content generation...")
        try:
            content = await agent.generate_content(
                topic="Linear Algebra Basics",
                difficulty_level="beginner",
                content_type="study-notes"
            )
            
            print("   ✅ Content generated successfully!")
            print(f"   📝 Content length: {len(content.get('content', ''))} characters")
            print(f"   🔑 Key concepts: {len(content.get('key_concepts', []))}")
            print(f"   📚 Study materials: {len(str(content.get('study_materials', {})))} characters")
            
            # Show a preview of the generated content
            content_preview = content.get('content', '')[:200]
            print(f"   📖 Content preview: {content_preview}...")
            
        except Exception as e:
            print(f"   ❌ Content generation failed: {str(e)}")
            return False
        
        print("\n🎉 Agent test completed successfully!")
        print("🚀 Your ContentGeneratorAgent is working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing TutorMind AI Agent with Environment Variables")
    print("=" * 60)
    
    success = asyncio.run(test_agent_with_env())
    
    if success:
        print("\n🎉 All tests passed! Your AI agent is ready to use!")
        print("💡 You can now:")
        print("   - Generate educational content using Gemini AI")
        print("   - Process content requests from the frontend")
        print("   - Store generated content in MongoDB")
        print("   - Display AI-generated content to users")
    else:
        print("\n💥 Some tests failed. Please check the errors above.")
        print("🔧 Common issues:")
        print("   - Missing or incorrect GEMINI_API_KEY in .env file")
        print("   - Network connectivity issues")
        print("   - Missing dependencies")
        sys.exit(1)


