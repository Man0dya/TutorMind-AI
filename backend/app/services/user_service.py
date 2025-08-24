from typing import Optional
from datetime import datetime
from app.models.user import UserCreate, UserInDB, UserResponse
from app.utils.database import get_collection
from app.utils.security import get_password_hash, verify_password, create_access_token
from bson import ObjectId

class UserService:
    def __init__(self):
        self.collection = get_collection("users")

    async def create_user(self, user: UserCreate) -> UserResponse:
        """Create a new user."""
        # Check if user already exists
        existing_user = await self.collection.find_one({"email": user.email.lower()})
        if existing_user:
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
        
        return UserResponse(**user_doc)

    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        """Authenticate a user with email and password."""
        user_doc = await self.collection.find_one({"email": email.lower()})
        if not user_doc:
            return None
        
        if not verify_password(password, user_doc["hashed_password"]):
            return None
        
        return UserResponse(**user_doc)

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get user by email."""
        user_doc = await self.collection.find_one({"email": email.lower()})
        if user_doc:
            return UserResponse(**user_doc)
        return None

    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get user by ID."""
        try:
            user_doc = await self.collection.find_one({"_id": ObjectId(user_id)})
            if user_doc:
                return UserResponse(**user_doc)
        except Exception:
            pass
        return None

    async def update_user(self, user_id: str, update_data: dict) -> Optional[UserResponse]:
        """Update user information."""
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_user_by_id(user_id)
        return None

    def create_user_token(self, user: UserResponse) -> str:
        """Create JWT token for user."""
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        return create_access_token(data=token_data)
