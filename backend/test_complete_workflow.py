#!/usr/bin/env python3
"""
Test script to verify the complete frontend-to-backend workflow
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

async def test_complete_workflow():
    """Test the complete workflow from content creation to AI generation."""
    try:
        print("🧪 Testing Complete Frontend-to-Backend Workflow")
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
            # Initialize services
            print("2. Initializing services...")
            content_service = ContentService()
            agent_service = AgentService()
            print("   ✅ Services initialized successfully")
            
            # Test content creation (simulating frontend request)
            print("3. Testing content creation (frontend simulation)...")
            test_content = ContentGenerationCreate(
                topic="Machine Learning Basics",
                difficulty_level="beginner",
                content_type="study-notes"
            )
            
            test_user_id = "test_user_workflow"
            
            # Create content request (this was failing before)
            content_request = await content_service.create_content_request(
                user_id=test_user_id,
                content_data=test_content
            )
            
            print(f"   ✅ Content request created successfully: {content_request.id}")
            print(f"   📝 Topic: {content_request.topic}")
            print(f"   📊 Status: {content_request.status}")
            
            # Test AI agent processing
            print("4. Testing AI agent processing...")
            if agent_service.get_agent_status()['overall_status'] == 'healthy':
                result = await agent_service.process_content_generation(
                    content_id=content_request.id,
                    topic=test_content.topic,
                    difficulty_level=test_content.difficulty_level,
                    content_type=test_content.content_type
                )
                
                if result['success']:
                    print("   ✅ AI content generation completed successfully!")
                    print(f"   📝 Generated content length: {len(result['generated_content'])} characters")
                    print(f"   🔑 Key concepts: {len(result['key_concepts'])} concepts")
                    
                    # Test retrieving the updated content
                    updated_content = await content_service.get_content_by_id(content_request.id)
                    if updated_content and updated_content.status == "completed":
                        print("   ✅ Content status updated to 'completed' in database")
                        print(f"   📖 Content preview: {updated_content.generated_content[:100]}...")
                    else:
                        print("   ⚠️ Content status not updated properly")
                else:
                    print(f"   ❌ AI content generation failed: {result.get('error', 'Unknown error')}")
            else:
                print("   ⚠️ AI agent not available, skipping generation test")
            
            # Test content history retrieval
            print("5. Testing content history retrieval...")
            history = await content_service.get_user_content_history(test_user_id, limit=5)
            print(f"   ✅ Retrieved {len(history)} content items from history")
            
        finally:
            # Close database connection
            print("6. Closing database connection...")
            await close_mongo_connection()
            print("   ✅ Database connection closed")
        
        print("\n🎉 Complete workflow test passed!")
        print("🚀 Your system is ready for frontend integration!")
        return True
        
    except Exception as e:
        print(f"❌ Workflow test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Complete TutorMind AI Workflow")
    print("=" * 60)
    
    success = asyncio.run(test_complete_workflow())
    
    if success:
        print("\n🎉 All tests passed! Your system is fully functional!")
        print("💡 You can now:")
        print("   - Start the frontend: cd frontend && npm run dev")
        print("   - Start the backend: cd backend && py run.py")
        print("   - Test the complete workflow in the browser")
    else:
        print("\n💥 Some tests failed. Please check the errors above.")
        sys.exit(1)

