from typing import Optional
from datetime import datetime
from app.models.user import UserCreate, UserInDB, UserResponse
from app.utils.database import get_collection
from app.utils.security import get_password_hash, verify_password, create_access_token
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self.collection = get_collection("users")

    def _prepare_user_response(self, user_doc: dict) -> dict:
        """Prepare user document for UserResponse by converting ObjectId to string."""
        response_doc = user_doc.copy()
        if "_id" in response_doc and isinstance(response_doc["_id"], ObjectId):
            response_doc["_id"] = str(response_doc["_id"])
        return response_doc

    async def create_user(self, user: UserCreate) -> UserResponse:
        """Create a new user in MongoDB Atlas."""
        try:
            # Check if user already exists
            existing_user = await self.collection.find_one({"email": user.email.lower()})
            if existing_user:
                logger.warning(f"User registration failed: Email {user.email} already exists")
                raise ValueError("User with this email already exists")
            
            # Create user document
            user_doc = {
                "email": user.email.lower(),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "hashed_password": get_password_hash(user.password),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_active": True,
                "avatar": None
            }
            
            result = await self.collection.insert_one(user_doc)
            user_doc["_id"] = result.inserted_id
            
            logger.info(f"✅ User created successfully: {user.email}")
            
            # Prepare response document with proper ObjectId conversion
            response_doc = self._prepare_user_response(user_doc)
            return UserResponse(**response_doc)
            
        except Exception as e:
            logger.error(f"❌ Error creating user {user.email}: {str(e)}")
            raise e

    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        """Authenticate a user with email and password from MongoDB Atlas."""
        try:
            user_doc = await self.collection.find_one({"email": email.lower()})
            if not user_doc:
                logger.warning(f"Login failed: Email {email} not found")
                return None
            
            if not verify_password(password, user_doc["hashed_password"]):
                logger.warning(f"Login failed: Invalid password for {email}")
                return None
            
            logger.info(f"✅ User authenticated successfully: {email}")
            
            # Prepare response document with proper ObjectId conversion
            response_doc = self._prepare_user_response(user_doc)
            return UserResponse(**response_doc)
            
        except Exception as e:
            logger.error(f"❌ Error authenticating user {email}: {str(e)}")
            return None

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get user by email from MongoDB Atlas."""
        try:
            user_doc = await self.collection.find_one({"email": email.lower()})
            if user_doc:
                response_doc = self._prepare_user_response(user_doc)
                return UserResponse(**response_doc)
            return None
        except Exception as e:
            logger.error(f"❌ Error getting user by email {email}: {str(e)}")
            return None

    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get user by ID from MongoDB Atlas."""
        try:
            user_doc = await self.collection.find_one({"_id": ObjectId(user_id)})
            if user_doc:
                response_doc = self._prepare_user_response(user_doc)
                return UserResponse(**response_doc)
        except Exception as e:
            logger.error(f"❌ Error getting user by ID {user_id}: {str(e)}")
        return None

    async def update_user(self, user_id: str, update_data: dict) -> Optional[UserResponse]:
        """Update user information in MongoDB Atlas."""
        try:
            update_data["updated_at"] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.modified_count:
                logger.info(f"✅ User updated successfully: {user_id}")
                return await self.get_user_by_id(user_id)
            return None
        except Exception as e:
            logger.error(f"❌ Error updating user {user_id}: {str(e)}")
            return None

    def create_user_token(self, user: UserResponse) -> str:
        """Create JWT token for user."""
        try:
            token_data = {
                "sub": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
            token = create_access_token(data=token_data)
            logger.info(f"✅ JWT token created for user: {user.email}")
            return token
        except Exception as e:
            logger.error(f"❌ Error creating JWT token for user {user.email}: {str(e)}")
            raise e
