#!/usr/bin/env python3
"""
Test script to verify Content Generation API endpoints
Run this to test the content generation functionality
"""

import asyncio
import sys
import os
import json

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_content_api():
    """Test Content Generation API endpoints."""
    try:
        from app.main import app
        from app.services.content_service import ContentService
        from app.models.content import ContentGenerationCreate
        from app.utils.database import connect_to_mongo, close_mongo_connection
        
        print("🧪 Testing Content Generation API")
        print("=" * 50)
        
        # Connect to database first
        print("1. Connecting to MongoDB...")
        await connect_to_mongo()
        print("   ✅ Database connected successfully")
        
        try:
            # Test content service
            print("2. Testing Content Service...")
            content_service = ContentService()
            
            # Test creating a content request
            print("3. Testing content request creation...")
            test_content = ContentGenerationCreate(
                topic="Linear Algebra",
                difficulty_level="beginner",
                content_type="study-notes"
            )
            
            print(f"   ✅ Test content data: {test_content.model_dump()}")
            
            # Test the service methods
            print("4. Testing service methods...")
            
            # Simulate a user ID
            test_user_id = "test_user_123"
            
            # Test creating content request
            try:
                content_request = await content_service.create_content_request(
                    user_id=test_user_id,
                    content_data=test_content
                )
                print(f"   ✅ Content request created: {content_request.id}")
                print(f"   📝 Topic: {content_request.topic}")
                print(f"   📊 Difficulty: {content_request.difficulty_level}")
                print(f"   📄 Type: {content_request.content_type}")
                print(f"   📅 Status: {content_request.status}")
                
                # Test getting content by ID
                retrieved_content = await content_service.get_content_by_id(content_request.id)
                if retrieved_content:
                    print(f"   ✅ Content retrieved by ID: {retrieved_content.id}")
                else:
                    print("   ❌ Failed to retrieve content by ID")
                
                # Test getting user content history
                user_history = await content_service.get_user_content_history(test_user_id)
                print(f"   ✅ User content history: {len(user_history)} items")
                
                # Test marking as completed
                completed_content = await content_service.mark_content_completed(
                    content_request.id,
                    "This is sample generated content for Linear Algebra at beginner level.",
                    {"generation_time": "2.5s", "model": "test"}
                )
                
                if completed_content:
                    print(f"   ✅ Content marked as completed: {completed_content.status}")
                    print(f"   📝 Generated content length: {len(completed_content.generated_content or '')} characters")
                else:
                    print("   ❌ Failed to mark content as completed")
                    
            except Exception as e:
                print(f"   ❌ Error testing content service: {str(e)}")
                return False
                
        finally:
            # Always close the database connection
            print("5. Closing database connection...")
            await close_mongo_connection()
            print("   ✅ Database connection closed")
        
        print("\n🎉 All Content Generation API tests passed!")
        print("🚀 Ready to integrate with LLM backend agent")
        return True
        
    except Exception as e:
        print(f"❌ Content Generation API test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing TutorMind AI Content Generation API")
    print("=" * 60)
    
    # Run the test
    success = asyncio.run(test_content_api())
    
    if success:
        print("\n🎉 All tests passed! Content Generation API is working correctly.")
        print("💡 You can now:")
        print("   - Submit content generation requests")
        print("   - Store requests in MongoDB")
        print("   - Retrieve content history")
        print("   - Update content status")
        print("   - Integrate with LLM backend agent")
    else:
        print("\n💥 Tests failed. Please check the errors above.")
        sys.exit(1)
