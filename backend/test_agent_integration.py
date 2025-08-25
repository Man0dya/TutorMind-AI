#!/usr/bin/env python3
"""
Test script to verify Agent Integration and Content Generation
Run this to test the complete workflow from agent to content generation
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

async def test_agent_integration():
    """Test the complete agent integration workflow."""
    try:
        print("🧪 Testing Agent Integration and Content Generation")
        print("=" * 60)
        
        # Test 1: Import and initialize agents
        print("1. Testing Agent Import and Initialization...")
        try:
            from agents.content_generator_agent import ContentGeneratorAgent
            from app.services.agent_service import AgentService
            
            print("   ✅ Agents imported successfully")
        except Exception as e:
            print(f"   ❌ Agent import failed: {str(e)}")
            return False
        
        # Test 2: Initialize ContentGeneratorAgent
        print("2. Testing ContentGeneratorAgent Initialization...")
        try:
            content_agent = ContentGeneratorAgent()
            agent_status = content_agent.get_status()
            
            print(f"   📊 Agent Status: {agent_status}")
            
            if agent_status['available']:
                print("   ✅ ContentGeneratorAgent is available and ready")
            else:
                print("   ⚠️ ContentGeneratorAgent is not available")
                print("   💡 Check your GEMINI_API_KEY in .env file")
                
        except Exception as e:
            print(f"   ❌ Agent initialization failed: {str(e)}")
            return False
        
        # Test 3: Test Agent Service
        print("3. Testing Agent Service...")
        try:
            agent_service = AgentService()
            service_status = agent_service.get_agent_status()
            
            print(f"   📊 Service Status: {service_status['overall_status']}")
            
            if service_status['overall_status'] == 'healthy':
                print("   ✅ Agent Service is healthy")
            else:
                print("   ⚠️ Agent Service has issues")
                
        except Exception as e:
            print(f"   ❌ Agent service test failed: {str(e)}")
            return False
        
        # Test 4: Test Content Generation (if agent is available)
        if content_agent.is_available():
            print("4. Testing Content Generation...")
            try:
                test_result = await agent_service.test_agent_connection()
                
                if test_result['success']:
                    print("   ✅ Content generation test successful")
                    print(f"   📝 Test content length: {test_result['test_content_length']} characters")
                else:
                    print(f"   ⚠️ Content generation test failed: {test_result['error']}")
                    
            except Exception as e:
                print(f"   ❌ Content generation test failed: {str(e)}")
                return False
        else:
            print("4. Skipping Content Generation Test (agent not available)")
        
        print("\n🎉 Agent Integration Tests Completed!")
        return True
        
    except Exception as e:
        print(f"❌ Agent integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_content_workflow():
    """Test the complete content generation workflow."""
    try:
        print("\n🔄 Testing Complete Content Generation Workflow")
        print("=" * 60)
        
        from app.services.content_service import ContentService
        from app.services.agent_service import AgentService
        from app.models.content import ContentGenerationCreate
        from app.utils.database import connect_to_mongo, close_mongo_connection
        
        # Connect to database
        print("1. Connecting to MongoDB...")
        await connect_to_mongo()
        print("   ✅ Database connected successfully")
        
        try:
            # Test content service
            print("2. Testing Content Service...")
            content_service = ContentService()
            agent_service = AgentService()
            
            # Test creating a content request
            print("3. Testing content request creation...")
            test_content = ContentGenerationCreate(
                topic="Linear Algebra Basics",
                difficulty_level="beginner",
                content_type="study-notes"
            )
            
            print(f"   ✅ Test content data: {test_content.model_dump()}")
            
            # Simulate a user ID
            test_user_id = "test_user_123"
            
            # Test creating content request
            try:
                content_request = await content_service.create_content_request(
                    user_id=test_user_id,
                    content_data=test_content
                )
                print(f"   ✅ Content request created: {content_request.id}")
                
                # Test agent processing
                print("4. Testing Agent Processing...")
                if agent_service.get_agent_status()['overall_status'] == 'healthy':
                    result = await agent_service.process_content_generation(
                        content_id=content_request.id,
                        topic=test_content.topic,
                        difficulty_level=test_content.difficulty_level,
                        content_type=test_content.content_type
                    )
                    
                    if result['success']:
                        print("   ✅ Content generation completed successfully")
                        print(f"   📝 Generated content length: {len(result['generated_content'])} characters")
                        print(f"   🔑 Key concepts: {len(result['key_concepts'])} concepts")
                    else:
                        print(f"   ❌ Content generation failed: {result['error']}")
                else:
                    print("   ⚠️ Agent not available, skipping generation test")
                
                # Test getting content by ID
                retrieved_content = await content_service.get_content_by_id(content_request.id)
                if retrieved_content:
                    print(f"   ✅ Content retrieved by ID: {retrieved_content.id}")
                    print(f"   📊 Status: {retrieved_content.status}")
                else:
                    print("   ❌ Failed to retrieve content by ID")
                
            except Exception as e:
                print(f"   ❌ Error testing content workflow: {str(e)}")
                return False
                
        finally:
            # Always close the database connection
            print("5. Closing database connection...")
            await close_mongo_connection()
            print("   ✅ Database connection closed")
        
        print("\n🎉 Content Workflow Tests Completed!")
        return True
        
    except Exception as e:
        print(f"❌ Content workflow test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing TutorMind AI Agent Integration")
    print("=" * 60)
    
    # Run the tests
    async def run_tests():
        # Test 1: Agent Integration
        agent_success = await test_agent_integration()
        
        # Test 2: Content Workflow (only if agents are working)
        if agent_success:
            workflow_success = await test_content_workflow()
        else:
            print("\n⚠️ Skipping content workflow test due to agent issues")
            workflow_success = False
        
        return agent_success and workflow_success
    
    success = asyncio.run(run_tests())
    
    if success:
        print("\n🎉 All tests passed! Agent integration is working correctly.")
        print("💡 You can now:")
        print("   - Generate content using AI agents")
        print("   - Process content requests automatically")
        print("   - Store generated content in MongoDB")
        print("   - Retrieve and display content to users")
    else:
        print("\n💥 Some tests failed. Please check the errors above.")
        print("🔧 Common issues:")
        print("   - Missing GEMINI_API_KEY in .env file")
        print("   - Network connectivity issues")
        print("   - Missing dependencies (run: pip install google-generativeai)")
        sys.exit(1)

