import json
import os
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Google Gemini AI integration
try:
    import google.generativeai as genai
    from google.generativeai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("Google Generative AI package not available. Install with: pip install google-generativeai")

logger = logging.getLogger(__name__)

class ContentGeneratorAgent:
    """
    Content Generator Agent for creating educational content using Google Gemini AI
    Processes content generation requests and returns structured educational content
    """
    
    def __init__(self):
        self.agent_id = "content_generator"
        self.model = None
        self.api_key = None
        
        # Initialize Gemini AI if available
        if GEMINI_AVAILABLE:
            self._initialize_gemini()
        else:
            logger.error("Gemini AI not available. Please install google-generativeai package.")
    
    def _initialize_gemini(self):
        """Initialize Google Gemini AI with API key"""
        try:
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                logger.error("GEMINI_API_KEY not found in environment variables")
                return
            
            genai.configure(api_key=self.api_key)
            
            # Use Gemini 2.0 Flash for content generation
            try:
                self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
                logger.info("✅ Gemini 2.0 Flash model initialized successfully")
            except Exception as e:
                # Fallback to Gemini 1.5 Pro if 2.0 is not available
                try:
                    self.model = genai.GenerativeModel('gemini-1.5-pro')
                    logger.info("✅ Gemini 1.5 Pro model initialized successfully (fallback)")
                except Exception as fallback_error:
                    logger.error(f"Failed to initialize Gemini models: {fallback_error}")
                    self.model = None
                    
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {e}")
            self.model = None
    
    async def generate_content(self, topic: str, difficulty_level: str, content_type: str, 
                             subject: str = "General", learning_objectives: Optional[list] = None) -> Dict[str, Any]:
        """
        Generate educational content using Gemini AI
        
        Args:
            topic (str): The topic to generate content for
            difficulty_level (str): Difficulty level (beginner, intermediate, advanced)
            content_type (str): Type of content to generate
            subject (str): Subject area (optional)
            learning_objectives (list): Specific learning goals (optional)
            
        Returns:
            dict: Generated educational content with metadata
        """
        try:
            if not self.model:
                raise Exception("Gemini AI model not initialized")
            
            logger.info(f"🔄 Generating content for topic: {topic}, difficulty: {difficulty_level}, type: {content_type}")
            
            # Generate the main content
            main_content = await self._generate_main_content(topic, difficulty_level, content_type, subject, learning_objectives)
            
            # Create study materials
            study_materials = await self._create_study_materials(topic, main_content, content_type)
            
            # Generate key concepts and summary
            key_concepts = await self._extract_key_concepts(topic, main_content)
            
            # Create comprehensive response
            result = {
                'content': main_content,
                'study_materials': study_materials,
                'key_concepts': key_concepts,
                'metadata': {
                    'topic': topic,
                    'difficulty_level': difficulty_level,
                    'content_type': content_type,
                    'subject': subject,
                    'generated_at': datetime.utcnow().isoformat(),
                    'model_used': 'gemini-2.0-flash-exp' if '2.0' in str(self.model) else 'gemini-1.5-pro',
                    'agent_id': self.agent_id
                }
            }
            
            logger.info(f"✅ Content generated successfully for topic: {topic}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Content generation failed for topic {topic}: {str(e)}")
            raise Exception(f"Content generation failed: {str(e)}")
    
    async def _generate_main_content(self, topic: str, difficulty_level: str, content_type: str, 
                                   subject: str, learning_objectives: Optional[list]) -> str:
        """Generate the main educational content"""
        
        # Map content types to specific generation styles
        content_styles = {
            "study-notes": "Create comprehensive study notes that are easy to follow and memorize. Use bullet points, clear headings, and practical examples.",
            "explanation": "Provide a detailed, step-by-step explanation that builds understanding progressively. Include analogies and real-world connections.",
            "summary": "Create a concise but comprehensive overview that captures the essence of the topic with key points highlighted.",
            "tutorial": "Write a hands-on tutorial with step-by-step guidance. Include practical examples and encourage experimentation.",
            "cheat-sheet": "Create a quick reference guide with essential information, formulas, and key concepts in an easy-to-scan format.",
            "mind-map": "Design a structured mind map with main concepts, sub-topics, and connections clearly outlined."
        }
        
        style_guide = content_styles.get(content_type, content_styles["explanation"])
        
        # Create the system prompt
        system_prompt = f"""You are an expert educator and content creator specializing in {subject}. 
        Create engaging, educational content that:
        - Is appropriate for {difficulty_level} level learners
        - Uses clear, accessible language
        - Includes relevant examples and real-world connections
        - Follows the {content_type} format effectively
        - Maintains educational value while being engaging
        
        Content Type: {content_type}
        Subject Area: {subject}
        Difficulty Level: {difficulty_level}
        Style Guide: {style_guide}
        """
        
        # Create the user prompt
        user_prompt = f"""Create comprehensive educational content about: {topic}
        
        {f"Learning Objectives: {', '.join(learning_objectives)}" if learning_objectives else ""}
        
        Requirements:
        - Write in a clear, educational style
        - Include an engaging introduction
        - Provide comprehensive explanations with examples
        - Use appropriate formatting for {content_type}
        - Include practical applications where relevant
        - End with a meaningful conclusion or summary
        
        Make the content engaging and easy to understand for {difficulty_level} level students.
        """
        
        try:
            # Generate content using Gemini AI
            response = await asyncio.to_thread(
                self.model.generate_content,
                f"{system_prompt}\n\n{user_prompt}"
            )
            
            if response and response.text:
                return response.text
            else:
                raise Exception("No content generated by Gemini AI")
                
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {e}")
            raise Exception(f"Content generation with Gemini failed: {str(e)}")
    
    async def _create_study_materials(self, topic: str, content: str, content_type: str) -> Dict[str, Any]:
        """Create additional study materials based on the generated content"""
        
        try:
            # Generate study materials prompt
            study_prompt = f"""Based on the following content about {topic}, create helpful study materials:

{content[:1000]}...

Create:
1. Key Points Summary (5-7 main points)
2. Important Definitions (3-5 key terms)
3. Study Tips (3-4 practical tips)
4. Practice Questions (2-3 questions to test understanding)

Format as a structured study guide."""
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                f"You are an expert educational content creator. {study_prompt}"
            )
            
            if response and response.text:
                study_materials = response.text
            else:
                study_materials = "Study materials could not be generated."
            
            return {
                'study_guide': study_materials,
                'content_type': content_type,
                'topic': topic
            }
            
        except Exception as e:
            logger.error(f"Error creating study materials: {e}")
            return {
                'study_guide': "Study materials could not be generated.",
                'content_type': content_type,
                'topic': topic
            }
    
    async def _extract_key_concepts(self, topic: str, content: str) -> list:
        """Extract key concepts from the generated content"""
        
        try:
            # Generate key concepts prompt
            concepts_prompt = f"""From the following content about {topic}, extract the 10 most important key concepts:

{content[:1000]}...

List only the key concept names, one per line, without explanations."""
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                f"You are an expert at identifying key concepts in educational content. {concepts_prompt}"
            )
            
            if response and response.text:
                # Parse the response to extract concepts
                concepts = [line.strip() for line in response.text.split('\n') if line.strip()]
                # Clean up and limit to 10 concepts
                concepts = [c for c in concepts if len(c) > 2 and len(c) < 100][:10]
                return concepts
            else:
                return [f"Key concept in {topic}"]
                
        except Exception as e:
            logger.error(f"Error extracting key concepts: {e}")
            return [f"Key concept in {topic}"]
    
    async def adapt_content_difficulty(self, content: str, target_difficulty: str) -> str:
        """Adapt existing content to different difficulty level"""
        
        try:
            adaptation_prompt = f"""Adapt the following educational content to {target_difficulty} level:

{content}

Adjust:
- Vocabulary complexity
- Concept depth
- Examples used
- Explanations detail

Make it appropriate for {target_difficulty} learners while maintaining accuracy."""
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                f"You are an expert at adapting educational content for different skill levels. {adaptation_prompt}"
            )
            
            if response and response.text:
                return response.text
            else:
                return "Content adaptation failed"
                
        except Exception as e:
            logger.error(f"Error adapting content difficulty: {e}")
            return "Content adaptation failed"
    
    def is_available(self) -> bool:
        """Check if the agent is available and properly configured"""
        return self.model is not None and self.api_key is not None
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent"""
        return {
            'agent_id': self.agent_id,
            'available': self.is_available(),
            'model_initialized': self.model is not None,
            'api_key_configured': self.api_key is not None,
            'gemini_available': GEMINI_AVAILABLE
        }
