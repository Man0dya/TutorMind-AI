from typing import Optional, List
from datetime import datetime
from app.models.content import ContentGeneration, ContentGenerationCreate, ContentGenerationUpdate, ContentGenerationResponse
from app.utils.database import get_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class ContentService:
    def __init__(self):
        self.collection = get_collection("content_generations")

    def _prepare_content_response(self, content_doc: dict) -> dict:
        """Prepare content document for response by converting ObjectId to string."""
        response_doc = content_doc.copy()
        if "_id" in response_doc:
            if isinstance(response_doc["_id"], ObjectId):
                response_doc["_id"] = str(response_doc["_id"])
            # Ensure the _id field is present for the alias mapping
            if "_id" not in response_doc:
                response_doc["_id"] = str(response_doc.get("id", ""))
        return response_doc

    async def create_content_request(self, user_id: str, content_data: ContentGenerationCreate) -> ContentGenerationResponse:
        """Create a new content generation request."""
        try:
            content_doc = {
                "user_id": user_id,
                "topic": content_data.topic,
                "difficulty_level": content_data.difficulty_level,
                "content_type": content_data.content_type,
                "status": "pending",
                "generated_content": None,
                "request_timestamp": datetime.utcnow(),
                "completion_timestamp": None,
                "error_message": None,
                "metadata": {}
            }
            
            result = await self.collection.insert_one(content_doc)
            content_doc["_id"] = result.inserted_id
            
            logger.info(f"✅ Content generation request created for user {user_id}: {content_data.topic}")
            
            return ContentGenerationResponse.from_mongo(content_doc)
            
        except Exception as e:
            logger.error(f"❌ Error creating content request for user {user_id}: {str(e)}")
            raise e

    async def get_content_by_id(self, content_id: str) -> Optional[ContentGenerationResponse]:
        """Get content generation by ID."""
        try:
            content_doc = await self.collection.find_one({"_id": ObjectId(content_id)})
            if content_doc:
                return ContentGenerationResponse.from_mongo(content_doc)
            return None
        except Exception as e:
            logger.error(f"❌ Error getting content by ID {content_id}: {str(e)}")
            return None

    async def get_user_content_history(self, user_id: str, limit: int = 20) -> List[ContentGenerationResponse]:
        """Get content generation history for a user."""
        try:
            cursor = self.collection.find({"user_id": user_id}).sort("request_timestamp", -1).limit(limit)
            content_list = []
            
            async for content_doc in cursor:
                content_list.append(ContentGenerationResponse.from_mongo(content_doc))
            
            logger.info(f"✅ Retrieved {len(content_list)} content items for user {user_id}")
            return content_list
            
        except Exception as e:
            logger.error(f"❌ Error getting content history for user {user_id}: {str(e)}")
            return []

    async def update_content_status(self, content_id: str, update_data: ContentGenerationUpdate) -> Optional[ContentGenerationResponse]:
        """Update content generation status and content."""
        try:
            update_fields = {}
            
            if update_data.status is not None:
                update_fields["status"] = update_data.status
                
            if update_data.generated_content is not None:
                update_fields["generated_content"] = update_data.generated_content
                
            if update_data.completion_timestamp is not None:
                update_fields["completion_timestamp"] = update_data.completion_timestamp
                
            if update_data.error_message is not None:
                update_fields["error_message"] = update_data.error_message
                
            if update_data.metadata is not None:
                update_fields["metadata"] = update_data.metadata

            if not update_fields:
                return None

            update_fields["updated_at"] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(content_id)},
                {"$set": update_fields}
            )
            
            if result.modified_count:
                logger.info(f"✅ Content {content_id} updated successfully")
                return await self.get_content_by_id(content_id)
            return None
            
        except Exception as e:
            logger.error(f"❌ Error updating content {content_id}: {str(e)}")
            return None

    async def mark_content_completed(self, content_id: str, generated_content: str, metadata: dict = None) -> Optional[ContentGenerationResponse]:
        """Mark content generation as completed with generated content."""
        try:
            update_data = ContentGenerationUpdate(
                status="completed",
                generated_content=generated_content,
                completion_timestamp=datetime.utcnow(),
                metadata=metadata or {}
            )
            
            return await self.update_content_status(content_id, update_data)
            
        except Exception as e:
            logger.error(f"❌ Error marking content {content_id} as completed: {str(e)}")
            return None

    async def mark_content_failed(self, content_id: str, error_message: str) -> Optional[ContentGenerationResponse]:
        """Mark content generation as failed with error message."""
        try:
            update_data = ContentGenerationUpdate(
                status="failed",
                error_message=error_message,
                completion_timestamp=datetime.utcnow()
            )
            
            return await self.update_content_status(content_id, update_data)
            
        except Exception as e:
            logger.error(f"❌ Error marking content {content_id} as failed: {str(e)}")
            return None

    async def get_pending_content_requests(self, limit: int = 10) -> List[ContentGenerationResponse]:
        """Get pending content generation requests for processing."""
        try:
            cursor = self.collection.find({"status": "pending"}).sort("request_timestamp", 1).limit(limit)
            content_list = []
            
            async for content_doc in cursor:
                response_doc = self._prepare_content_response(content_doc)
                content_list.append(ContentGenerationResponse(**response_doc))
            
            logger.info(f"✅ Retrieved {len(content_list)} pending content requests")
            return content_list
            
        except Exception as e:
            logger.error(f"❌ Error getting pending content requests: {str(e)}")
            return []

    async def delete_content(self, content_id: str, user_id: str) -> bool:
        """Delete content generation (only by the user who created it)."""
        try:
            result = await self.collection.delete_one({
                "_id": ObjectId(content_id),
                "user_id": user_id
            })
            
            if result.deleted_count:
                logger.info(f"✅ Content {content_id} deleted by user {user_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Error deleting content {content_id}: {str(e)}")
            return False
