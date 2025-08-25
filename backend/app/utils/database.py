from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db = None

async def connect_to_mongo():
    """Create database connection to MongoDB Atlas."""
    try:
        # Connect to MongoDB Atlas
        Database.client = AsyncIOMotorClient(
            settings.mongodb_uri,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=10000,         # 10 second connection timeout
            socketTimeoutMS=10000,          # 10 second socket timeout
            maxPoolSize=10,                 # Connection pool size
            minPoolSize=1                   # Minimum connections
        )
        
        # Test the connection
        await Database.client.admin.command('ping')
        
        # Get database instance
        Database.db = Database.client[settings.mongodb_db_name]
        
        logger.info(f"✅ Successfully connected to MongoDB Atlas")
        logger.info(f"📊 Database: {settings.mongodb_db_name}")
        logger.info(f"🔗 Cluster: cluster0.uvtm7dl.mongodb.net")
        
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
        raise e

async def close_mongo_connection():
    """Close database connection."""
    if Database.client:
        Database.client.close()
        logger.info("🔌 Closed MongoDB connection.")

def get_database():
    """Get database instance."""
    return Database.db

def get_collection(collection_name: str):
    """Get collection instance."""
    return Database.db[collection_name]
