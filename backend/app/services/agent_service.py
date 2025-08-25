from typing import Optional, Dict, Any
from app.models.content import ContentGenerationUpdate
from app.services.content_service import ContentService
from agents.content_generator_agent import ContentGeneratorAgent
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class AgentService:
    """Service for managing AI agents and their interactions"""
    
    def __init__(self):
        self.content_agent = ContentGeneratorAgent()
        self._content_service = None  # Lazy initialization
    
    @property
    def content_service(self):
        """Lazy initialization of ContentService to avoid database connection issues during import."""
        if self._content_service is None:
            try:
                self._content_service = ContentService()
            except Exception as e:
                logger.error(f"Failed to initialize ContentService: {e}")
                raise Exception(f"ContentService initialization failed: {str(e)}")
        return self._content_service
    
    async def process_content_generation(self, content_id: str, topic: str, difficulty_level: str, 
                                       content_type: str, subject: str = "General") -> Dict[str, Any]:
        """
        Process content generation request using the ContentGeneratorAgent
        
        Args:
            content_id (str): ID of the content generation request
            topic (str): Topic to generate content for
            difficulty_level (str): Difficulty level
            content_type (str): Type of content to generate
            subject (str): Subject area
            
        Returns:
            dict: Generated content and metadata
        """
        try:
            logger.info(f"🔄 Processing content generation request {content_id} for topic: {topic}")
            
            # Check if agent is available
            if not self.content_agent.is_available():
                raise Exception("ContentGeneratorAgent is not available")
            
            # Update status to processing
            await self.content_service.update_content_status(
                content_id,
                ContentGenerationUpdate(status="processing")
            )
            
            # Generate content using the agent
            generated_content = await self.content_agent.generate_content(
                topic=topic,
                difficulty_level=difficulty_level,
                content_type=content_type,
                subject=subject
            )
            
            # Extract the main content
            main_content = generated_content.get('content', '')
            study_materials = generated_content.get('study_materials', {})
            key_concepts = generated_content.get('key_concepts', [])
            metadata = generated_content.get('metadata', {})
            
            # Update the content in the database
            update_data = ContentGenerationUpdate(
                status="completed",
                generated_content=main_content,
                metadata={
                    **metadata,
                    'study_materials': study_materials,
                    'key_concepts': key_concepts,
                    'agent_used': 'ContentGeneratorAgent'
                }
            )
            
            updated_content = await self.content_service.update_content_status(content_id, update_data)
            
            if not updated_content:
                raise Exception("Failed to update content status after generation")
            
            logger.info(f"✅ Content generation completed successfully for request {content_id}")
            
            return {
                'success': True,
                'content_id': content_id,
                'generated_content': main_content,
                'study_materials': study_materials,
                'key_concepts': key_concepts,
                'metadata': metadata
            }
            
        except Exception as e:
            logger.error(f"❌ Content generation failed for request {content_id}: {str(e)}")
            
            # Update status to failed
            try:
                await self.content_service.update_content_status(
                    content_id,
                    ContentGenerationUpdate(
                        status="failed",
                        error_message=str(e)
                    )
                )
            except Exception as update_error:
                logger.error(f"Failed to update error status: {update_error}")
            
            return {
                'success': False,
                'content_id': content_id,
                'error': str(e)
            }
    
    async def regenerate_content(self, content_id: str) -> Dict[str, Any]:
        """
        Regenerate content for an existing request
        
        Args:
            content_id (str): ID of the content to regenerate
            
        Returns:
            dict: Regeneration result
        """
        try:
            logger.info(f"🔄 Regenerating content for request {content_id}")
            
            # Get the existing content
            existing_content = await self.content_service.get_content_by_id(content_id)
            if not existing_content:
                raise Exception("Content not found")
            
            # Process regeneration
            result = await self.process_content_generation(
                content_id=content_id,
                topic=existing_content.topic,
                difficulty_level=existing_content.difficulty_level,
                content_type=existing_content.content_type,
                subject="General"  # Could be enhanced to extract from metadata
            )
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Content regeneration failed for request {content_id}: {str(e)}")
            return {
                'success': False,
                'content_id': content_id,
                'error': str(e)
            }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get the status of all agents"""
        try:
            return {
                'content_generator': self.content_agent.get_status(),
                'overall_status': 'healthy' if self.content_agent.is_available() else 'degraded'
            }
        except Exception as e:
            logger.error(f"Error getting agent status: {e}")
            return {
                'content_generator': {'error': str(e)},
                'overall_status': 'error'
            }
    
    async def test_agent_connection(self) -> Dict[str, Any]:
        """Test the connection and functionality of the ContentGeneratorAgent"""
        try:
            status = self.content_agent.get_status()
            
            if not status.get('available', False):
                return {
                    'success': False,
                    'error': 'Agent not available',
                    'details': status
                }
            
            # Test with a simple content generation
            test_result = await self.content_agent.generate_content(
                topic="Test Topic",
                difficulty_level="beginner",
                content_type="summary",
                subject="General"
            )
            
            if test_result and test_result.get('content'):
                return {
                    'success': True,
                    'message': 'Agent connection test successful',
                    'test_content_length': len(test_result['content']),
                    'details': status
                }
            else:
                return {
                    'success': False,
                    'error': 'Agent test generation failed',
                    'details': status
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Agent test failed: {str(e)}',
                'details': self.content_agent.get_status()
            }
