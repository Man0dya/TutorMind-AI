from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from app.models.content import ContentGenerationCreate, ContentGenerationResponse, ContentGenerationUpdate
from app.models.user import UserResponse
from app.services.content_service import ContentService
from app.services.agent_service import AgentService
from app.routes.auth import get_current_user
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/content", tags=["content"])

@router.post("/generate", response_model=ContentGenerationResponse, status_code=status.HTTP_201_CREATED)
async def create_content_request(
    content_data: ContentGenerationCreate,
    background_tasks: BackgroundTasks,
    current_user: UserResponse = Depends(get_current_user)
):
    """Create a new content generation request and trigger AI generation."""
    try:
        logger.info(f"🔄 Content generation request from user {current_user.id}: {content_data.topic}")
        
        content_service = ContentService()
        agent_service = AgentService()
        
        # Create the content request in database
        content_request = await content_service.create_content_request(
            user_id=current_user.id,
            content_data=content_data
        )
        
        logger.info(f"✅ Content request created successfully: {content_request.id}")
        
        # Add background task to generate content using AI agent
        background_tasks.add_task(
            agent_service.process_content_generation,
            content_id=content_request.id,
            topic=content_data.topic,
            difficulty_level=content_data.difficulty_level,
            content_type=content_data.content_type
        )
        
        logger.info(f"🚀 Background task added for AI content generation: {content_request.id}")
        
        return content_request
        
    except Exception as e:
        logger.error(f"💥 Error creating content request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create content request: {str(e)}"
        )

@router.get("/history", response_model=List[ContentGenerationResponse])
async def get_content_history(
    limit: int = 20,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get content generation history for the current user."""
    try:
        logger.info(f"📚 Retrieving content history for user {current_user.id}")
        
        content_service = ContentService()
        content_history = await content_service.get_user_content_history(
            user_id=current_user.id,
            limit=limit
        )
        
        logger.info(f"✅ Retrieved {len(content_history)} content items for user {current_user.id}")
        return content_history
        
    except Exception as e:
        logger.error(f"💥 Error retrieving content history: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve content history: {str(e)}"
        )

@router.get("/{content_id}", response_model=ContentGenerationResponse)
async def get_content_by_id(
    content_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get specific content generation by ID."""
    try:
        logger.info(f"🔍 Retrieving content {content_id} for user {current_user.id}")
        
        content_service = ContentService()
        content = await content_service.get_content_by_id(content_id)
        
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found"
            )
        
        # Ensure user can only access their own content
        if content.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this content"
            )
        
        logger.info(f"✅ Content {content_id} retrieved successfully for user {current_user.id}")
        return content
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error retrieving content {content_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve content: {str(e)}"
        )

@router.put("/{content_id}", response_model=ContentGenerationResponse)
async def update_content(
    content_id: str,
    update_data: ContentGenerationUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Update content generation (admin or owner only)."""
    try:
        logger.info(f"🔄 Updating content {content_id} by user {current_user.id}")
        
        content_service = ContentService()
        
        # First check if content exists and user has access
        existing_content = await content_service.get_content_by_id(content_id)
        if not existing_content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found"
            )
        
        if existing_content.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to update this content"
            )
        
        updated_content = await content_service.update_content_status(content_id, update_data)
        
        if not updated_content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found or no changes made"
            )
        
        logger.info(f"✅ Content {content_id} updated successfully by user {current_user.id}")
        return updated_content
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error updating content {content_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update content: {str(e)}"
        )

@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    content_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Delete content generation (owner only)."""
    try:
        logger.info(f"🗑️ Deleting content {content_id} by user {current_user.id}")
        
        content_service = ContentService()
        
        # First check if content exists and user has access
        existing_content = await content_service.get_content_by_id(content_id)
        if not existing_content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found"
            )
        
        if existing_content.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to delete this content"
            )
        
        success = await content_service.delete_content(content_id, current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found or could not be deleted"
            )
        
        logger.info(f"✅ Content {content_id} deleted successfully by user {current_user.id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error deleting content {content_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete content: {str(e)}"
        )

@router.post("/{content_id}/regenerate", response_model=ContentGenerationResponse)
async def regenerate_content(
    content_id: str,
    background_tasks: BackgroundTasks,
    current_user: UserResponse = Depends(get_current_user)
):
    """Regenerate content for an existing request using AI agent."""
    try:
        logger.info(f"🔄 Regenerating content {content_id} for user {current_user.id}")
        
        content_service = ContentService()
        agent_service = AgentService()
        
        # First check if content exists and user has access
        existing_content = await content_service.get_content_by_id(content_id)
        if not existing_content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found"
            )
        
        if existing_content.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to regenerate this content"
            )
        
        # Reset status to pending for regeneration
        update_data = ContentGenerationUpdate(status="pending")
        updated_content = await content_service.update_content_status(content_id, update_data)
        
        if not updated_content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found or could not be updated"
            )
        
        # Add background task to regenerate content using AI agent
        background_tasks.add_task(
            agent_service.regenerate_content,
            content_id=content_id
        )
        
        logger.info(f"✅ Content {content_id} marked for regeneration by user {current_user.id}")
        logger.info(f"🚀 Background task added for AI content regeneration: {content_id}")
        
        return updated_content
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error regenerating content {content_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to regenerate content: {str(e)}"
        )

@router.get("/agents/status")
async def get_agents_status():
    """Get the status of all AI agents."""
    try:
        agent_service = AgentService()
        status = agent_service.get_agent_status()
        
        logger.info(f"📊 Agent status retrieved: {status['overall_status']}")
        return status
        
    except Exception as e:
        logger.error(f"💥 Error retrieving agent status: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve agent status: {str(e)}"
        )

@router.post("/agents/test")
async def test_agents():
    """Test the connection and functionality of AI agents."""
    try:
        logger.info("🧪 Testing AI agents connection and functionality")
        
        agent_service = AgentService()
        test_result = await agent_service.test_agent_connection()
        
        if test_result['success']:
            logger.info("✅ Agent test completed successfully")
        else:
            logger.warning(f"⚠️ Agent test completed with issues: {test_result['error']}")
        
        return test_result
        
    except Exception as e:
        logger.error(f"💥 Error testing agents: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to test agents: {str(e)}"
        )
