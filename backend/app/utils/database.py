from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

async def connect_to_mongo():
    """Create database connection."""
    Database.client = AsyncIOMotorClient(settings.mongodb_uri)
    Database.db = Database.client[settings.mongodb_db_name]
    print(f"Connected to MongoDB: {settings.mongodb_uri}")
    print(f"Database: {settings.mongodb_db_name}")

async def close_mongo_connection():
    """Close database connection."""
    if Database.client:
        Database.client.close()
        print("Closed MongoDB connection.")

def get_database():
    """Get database instance."""
    return Database.db

def get_collection(collection_name: str):
    """Get collection instance."""
    return Database.db[collection_name]
