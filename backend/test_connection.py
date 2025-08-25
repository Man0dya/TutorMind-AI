#!/usr/bin/env python3
"""
Test script to verify MongoDB Atlas connection
Run this before starting the main server to ensure database connectivity
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_mongodb_connection():
    """Test MongoDB Atlas connection."""
    try:
        from app.utils.database import connect_to_mongo, close_mongo_connection
        from app.config import settings
        
        print("🔍 Testing MongoDB Atlas connection...")
        print(f"📡 URI: {settings.mongodb_uri}")
        print(f"🗄️  Database: {settings.mongodb_db_name}")
        
        # Test connection
        await connect_to_mongo()
        
        print("✅ MongoDB Atlas connection successful!")
        print("🚀 Ready to start the server")
        
        # Close connection
        await close_mongo_connection()
        
    except Exception as e:
        print(f"❌ MongoDB Atlas connection failed: {str(e)}")
        print("🔧 Please check your connection string and network connectivity")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Testing TutorMind AI Backend Configuration")
    print("=" * 50)
    
    # Run the test
    success = asyncio.run(test_mongodb_connection())
    
    if success:
        print("\n🎉 All tests passed! You can now start the server.")
        print("💡 Run: python run.py")
    else:
        print("\n💥 Tests failed. Please fix the issues before starting the server.")
        sys.exit(1)
