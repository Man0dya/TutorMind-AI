#!/usr/bin/env python3
"""
Simple test script to debug the agent service issue
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

async def test_agent_service():
    """Test the agent service step by step."""
    try:
        print("🧪 Agent Service Test")
        print("=" * 40)
        
        # Test 1: Import AgentService
        print("1. Testing AgentService import...")
        try:
            from app.services.agent_service import AgentService
            print("   ✅ AgentService imported successfully")
        except Exception as e:
            print(f"   ❌ Import failed: {str(e)}")
            return False
        
        # Test 2: Initialize AgentService
        print("2. Testing AgentService initialization...")
        try:
            agent_service = AgentService()
            print("   ✅ AgentService initialized successfully")
        except Exception as e:
            print(f"   ❌ Initialization failed: {str(e)}")
            return False
        
        # Test 3: Check agent status
        print("3. Testing agent status...")
        try:
            status = agent_service.get_agent_status()
            print(f"   📊 Status: {status}")
            
            if status and 'overall_status' in status:
                print(f"   ✅ Overall status: {status['overall_status']}")
            else:
                print("   ❌ Status is missing expected fields")
                print(f"   🔍 Status keys: {list(status.keys()) if status else 'None'}")
                return False
                
        except Exception as e:
            print(f"   ❌ Status check failed: {str(e)}")
            return False
        
        # Test 4: Test agent connection
        print("4. Testing agent connection...")
        try:
            test_result = await agent_service.test_agent_connection()
            print(f"   📊 Test result: {test_result}")
            
            if test_result and 'success' in test_result:
                if test_result['success']:
                    print("   ✅ Agent connection test successful")
                    print(f"   📝 Test content length: {test_result.get('test_content_length', 'N/A')}")
                else:
                    print(f"   ⚠️ Agent connection test failed: {test_result.get('error', 'Unknown error')}")
            else:
                print("   ❌ Test result is missing expected fields")
                print(f"   🔍 Result keys: {list(test_result.keys()) if test_result else 'None'}")
                
        except Exception as e:
            print(f"   ❌ Agent connection test failed: {str(e)}")
            return False
        
        print("\n🎉 Agent service test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Agent Service")
    print("=" * 40)
    
    success = asyncio.run(test_agent_service())
    
    if success:
        print("\n🎉 Agent service is working correctly!")
        print("💡 You can now use it for content generation workflows.")
    else:
        print("\n💥 Agent service test failed. Please check the errors above.")
        sys.exit(1)

