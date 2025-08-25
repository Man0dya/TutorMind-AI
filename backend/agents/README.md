# AI Agents for TutorMind AI

This folder contains the AI agents that power the content generation capabilities of TutorMind AI.

## 🚀 Available Agents

### ContentGeneratorAgent
- **Purpose**: Generates educational content using Google Gemini AI
- **Capabilities**: 
  - Creates study notes, explanations, summaries, tutorials, cheat sheets, and mind maps
  - Adapts content to different difficulty levels (beginner, intermediate, advanced)
  - Generates study materials and key concepts
  - Integrates with MongoDB for content storage

## 📋 Prerequisites

### 1. Google Gemini API Key
You need a Google Gemini API key to use the ContentGeneratorAgent:

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file:
   ```env
   GEMINI_API_KEY=your-actual-api-key-here
   ```

### 2. Python Dependencies
Install the required packages:
```bash
pip install google-generativeai
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

## 🔧 Configuration

### Environment Variables
Add these to your `.env` file:
```env
# AI Agent Configuration
GEMINI_API_KEY=your-gemini-api-key-here
```

### Model Selection
The agent automatically selects the best available Gemini model:
1. **Primary**: Gemini 2.0 Flash (latest and fastest)
2. **Fallback**: Gemini 1.5 Pro (if 2.0 is not available)

## 📱 Usage

### Basic Content Generation
```python
from agents.content_generator_agent import ContentGeneratorAgent

# Initialize the agent
agent = ContentGeneratorAgent()

# Generate content
content = await agent.generate_content(
    topic="Linear Algebra",
    difficulty_level="beginner",
    content_type="study-notes"
)
```

### Through the API Service
```python
from app.services.agent_service import AgentService

# Initialize the service
agent_service = AgentService()

# Process content generation
result = await agent_service.process_content_generation(
    content_id="content_id",
    topic="Linear Algebra",
    difficulty_level="beginner",
    content_type="study-notes"
)
```

## 🎯 Content Types

The agent supports various content types:

| Type | Description | Best For |
|------|-------------|----------|
| `study-notes` | Comprehensive study notes with bullet points | Exam preparation |
| `explanation` | Detailed step-by-step explanations | Learning new concepts |
| `summary` | Concise overview with key points | Quick revision |
| `tutorial` | Hands-on step-by-step guide | Practical learning |
| `cheat-sheet` | Quick reference guide | Fast lookup |
| `mind-map` | Visual concept organization | Understanding relationships |

## 🔄 Workflow

1. **User submits form** → Frontend sends request to `/api/v1/content/generate`
2. **Backend creates request** → Stores in MongoDB with status "pending"
3. **Background task starts** → AgentService processes the request
4. **AI generation** → ContentGeneratorAgent uses Gemini AI to create content
5. **Content storage** → Generated content is stored in MongoDB
6. **Status update** → Content status is updated to "completed"
7. **Frontend display** → User can view the generated content

## 🧪 Testing

### Test Agent Integration
```bash
python test_agent_integration.py
```

### Test Complete Workflow
```bash
python test_content_workflow.py
```

### Test API Endpoints
```bash
# Test agent status
curl http://localhost:8000/api/v1/content/agents/status

# Test agent functionality
curl -X POST http://localhost:8000/api/v1/content/agents/test
```

## 📊 Monitoring

### Agent Status Endpoint
`GET /api/v1/content/agents/status`

Returns:
```json
{
  "content_generator": {
    "agent_id": "content_generator",
    "available": true,
    "model_initialized": true,
    "api_key_configured": true,
    "gemini_available": true
  },
  "overall_status": "healthy"
}
```

### Agent Test Endpoint
`POST /api/v1/content/agents/test`

Tests the agent's connection and functionality.

## 🚨 Troubleshooting

### Common Issues

1. **"Agent not available"**
   - Check your `GEMINI_API_KEY` in `.env` file
   - Verify the API key is valid and has sufficient quota

2. **"Gemini AI not available"**
   - Install the package: `pip install google-generativeai`
   - Check your internet connection

3. **"Content generation failed"**
   - Check the agent status endpoint
   - Verify MongoDB connection
   - Check server logs for detailed error messages

### Debug Mode
Enable debug logging in your `.env`:
```env
DEBUG=True
```

## 🔮 Future Enhancements

- **Multiple AI Providers**: Support for OpenAI, Claude, and other LLMs
- **Content Templates**: Pre-defined templates for different subjects
- **Quality Control**: AI-powered content validation and improvement
- **Batch Processing**: Handle multiple content requests simultaneously
- **Content Caching**: Cache frequently requested content for faster response

## 📚 API Reference

### ContentGeneratorAgent Methods

- `generate_content(topic, difficulty_level, content_type, subject, learning_objectives)`
- `adapt_content_difficulty(content, target_difficulty)`
- `is_available()`
- `get_status()`

### AgentService Methods

- `process_content_generation(content_id, topic, difficulty_level, content_type, subject)`
- `regenerate_content(content_id)`
- `get_agent_status()`
- `test_agent_connection()`

## 🤝 Contributing

To add new agents:

1. Create a new agent class in the `agents/` folder
2. Implement the required interface methods
3. Add the agent to the `AgentService`
4. Create tests for the new agent
5. Update this README with usage instructions

## 📄 License

This project is part of TutorMind AI and follows the same license terms.

