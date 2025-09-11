# Exercise 1: First AI Chat Service

## Objective
Create your first AI chat service using Azure OpenAI with different SDK approaches and learn to build interactive chat interfaces.

## What You'll Learn
- Azure OpenAI service setup and authentication
- Different SDK approaches (Azure OpenAI SDK vs OpenAI SDK)
- Basic chat completions API usage
- Interactive web interfaces with Chainlit
- Prompt engineering fundamentals
- Response handling and token management

## Prerequisites
- Azure subscription with OpenAI access
- Azure OpenAI resource deployed with a chat model (e.g., GPT-4)
- Python environment with required packages
- Environment variables configured (.env file)

## Structure
```
EX1-FirstAIChat/
├── README.md                 # This file
├── samples/                  # Code examples
│   ├── ex1-s1-aoai.py       # Azure OpenAI SDK example
│   ├── ex1-s1-oai.py        # Standard OpenAI SDK example
│   ├── ex1-s2-chainlit.py   # Interactive Chainlit web interface
│   ├── chainlit.md          # Chainlit interface configuration
│   └── public/              # Static assets for Chainlit
└── challenge/               # Practice challenges
    ├── challenge-1-azure-openai-personal-assistant.md
    └── challenge-2-chainlit-learning-companion.md
```

## Sample Applications

### 1. Azure OpenAI SDK Example (`ex1-s1-aoai.py`)
A straightforward example demonstrating:
- Azure OpenAI client setup and authentication
- Basic chat completion request with detailed parameter explanations
- Response handling and token usage analysis
- Comprehensive comments explaining each parameter and concept

**Key Features:**
- Direct Azure OpenAI SDK usage
- Detailed parameter documentation
- Token usage tracking
- Error handling best practices

### 2. Standard OpenAI SDK Example (`ex1-s1-oai.py`)
Shows how to use the standard OpenAI SDK with Azure OpenAI:
- Alternative authentication approach
- Standard OpenAI SDK syntax with Azure endpoints
- Comparison with Azure-specific SDK

**Key Features:**
- Standard OpenAI SDK compatibility
- Azure OpenAI integration
- Familiar OpenAI SDK patterns

### 3. Interactive Chainlit Interface (`ex1-s2-chainlit.py`)
A modern web-based chat interface featuring:
- Real-time streaming responses
- Conversation history management
- Session state handling
- Professional chat UI with Chainlit

**Key Features:**
- Web-based interactive interface
- Real-time message streaming
- Session persistence
- Event-driven architecture
- Multiple concurrent user support

## Challenges

### Challenge 1: Personal Assistant with Context Memory
Build an intelligent personal assistant using Azure OpenAI SDK that:
- Remembers user information across conversations
- Provides personalized responses
- Implements special commands for user management
- Handles persistent data storage

**Difficulty Levels:** Beginner → Intermediate → Advanced

### Challenge 2: AI-Powered Learning Companion with Chainlit
Create an adaptive learning system that:
- Identifies user learning styles through assessment
- Adapts teaching methods accordingly
- Supports multimedia content
- Tracks learning progress

**Difficulty Levels:** Beginner → Intermediate → Advanced

## Getting Started

1. **Environment Setup**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   Create a `.env` file with:
   ```
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
   AZURE_OPENAI_API_VERSION=2024-08-01-preview
   ```

3. **Run Sample Applications**
   ```bash
   # Basic Azure OpenAI example
   python samples/ex1-s1-aoai.py
   
   # Standard OpenAI SDK example
   python samples/ex1-s1-oai.py
   
   # Interactive Chainlit interface
   chainlit run samples/ex1-s2-chainlit.py
   ```

4. **Try the Challenges**
   - Start with Challenge 1 for Azure OpenAI SDK practice
   - Move to Challenge 2 for Chainlit and advanced features

## Learning Path
1. **Start Here**: Run and understand `ex1-s1-aoai.py`
2. **Compare Approaches**: Explore `ex1-s1-oai.py` 
3. **Interactive Experience**: Launch `ex1-s2-chainlit.py`
4. **Practice**: Complete challenges based on your interest
5. **Experiment**: Modify parameters and prompts to see different behaviors

## Key Concepts Covered
- **Authentication**: Azure OpenAI client setup
- **Chat Completions**: Message roles and conversation structure
- **Parameters**: Temperature, tokens, penalties explained
- **Streaming**: Real-time response delivery
- **Session Management**: State persistence across interactions
- **Error Handling**: Robust application patterns
- **User Experience**: Professional chat interfaces

This exercise provides a comprehensive foundation for building AI-powered chat applications!
