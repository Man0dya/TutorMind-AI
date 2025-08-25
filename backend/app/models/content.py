from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> dict[str, Any]:
        return {
            "type": "string",
            "validator": cls._validate,
        }

    @classmethod
    def _validate(cls, v: Any) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if ObjectId.is_valid(v):
                return ObjectId(v)
        raise ValueError("Invalid ObjectId")

class ContentRequest(BaseModel):
    """Model for content generation request"""
    topic: str = Field(..., min_length=1, max_length=200)
    difficulty_level: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    content_type: str = Field(..., min_length=1, max_length=50)
    user_id: str = Field(..., min_length=1)

class ContentGeneration(BaseModel):
    """Model for content generation with request details"""
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str = Field(..., min_length=1)
    topic: str = Field(..., min_length=1, max_length=200)
    difficulty_level: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    content_type: str = Field(..., min_length=1, max_length=50)
    status: str = Field(default="pending", pattern="^(pending|processing|completed|failed)$")
    generated_content: Optional[str] = None
    request_timestamp: datetime = Field(default_factory=datetime.utcnow)
    completion_timestamp: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata: Optional[dict] = {}

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class ContentGenerationResponse(BaseModel):
    """Response model for content generation"""
    id: str = Field(alias="_id")
    user_id: str
    topic: str
    difficulty_level: str
    content_type: str
    status: str
    generated_content: Optional[str] = None
    request_timestamp: datetime
    completion_timestamp: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata: Optional[dict] = {}

    @classmethod
    def from_mongo(cls, data: dict):
        """Create a ContentGenerationResponse from MongoDB document"""
        if not data:
            return None
        
        # Ensure _id is properly converted to string
        if "_id" in data:
            if isinstance(data["_id"], ObjectId):
                data["_id"] = str(data["_id"])
        
        return cls(**data)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class ContentGenerationCreate(BaseModel):
    """Model for creating new content generation request"""
    topic: str = Field(..., min_length=1, max_length=200)
    difficulty_level: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    content_type: str = Field(..., min_length=1, max_length=50)

class ContentGenerationUpdate(BaseModel):
    """Model for updating content generation"""
    status: Optional[str] = Field(None, pattern="^(pending|processing|completed|failed)$")
    generated_content: Optional[str] = None
    completion_timestamp: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata: Optional[dict] = {}
