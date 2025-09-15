# 0. Import necessary libraries and set up environment variables
# ---------------------------------------------------------------------
# This example demonstrates how to create and use an AI Agent using Azure AI Foundry
# with a Chainlit web interface. This combines the agent capabilities with a modern
# chat interface for interactive conversations.
# ---------------------------------------------------------------------
import os
import chainlit as cl
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# 1. Environment Variables Setup
# ---------------------------------------------------------------------
azure_foundry_project_endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")
azure_foundry_key = os.getenv("AI_FOUNDRY_API_KEY")
azure_foundry_deployment = os.getenv("AI_FOUNDRY_DEPLOYMENT_NAME")

# 2. Authentication Setup using DefaultAzureCredential
# ---------------------------------------------------------------------
# DefaultAzureCredential automatically discovers and uses the best available credential:
#   1. Environment variables (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)
#   2. Managed Identity (for Azure-hosted applications)  
#   3. Visual Studio Code authentication
#   4. Azure CLI authentication (`az login`)
#   5. Interactive browser authentication (fallback)
#
# Perfect for development environments where you're already authenticated
# via Azure CLI or VS Code. No need to manage secrets locally.
# ---------------------------------------------------------------------

# 3. AI Project Client Setup
# ---------------------------------------------------------------------
project = AIProjectClient(
    endpoint=azure_foundry_project_endpoint,
    credential=DefaultAzureCredential()
)

# 4. ChainLit Event Handlers for Interactive Chat
# ---------------------------------------------------------------------
# ChainLit provides decorators to handle different events in the chat interface:
# - @cl.on_chat_start: Called when a new chat session begins
# - @cl.on_message: Called when the user sends a message
# - @cl.on_chat_end: Called when the chat session ends
# ---------------------------------------------------------------------

@cl.on_chat_start
async def start():
    """
    This function is called when a new chat session starts.
    It initializes the AI Agent and creates a new conversation thread.
    """
    try:
        # Send a welcome message to the user
        await cl.Message(
            content="🤖 Hello! I'm your IBM Super Cool Agent powered by Azure AI Foundry. "
                    "I'm here to help you with any questions you may have. "
                    "Feel free to ask me anything!",
            author="IBM Agent"
        ).send()
        
        # 5. Agent Creation
        # ---------------------------------------------------------------------
        # Create an agent with specific instructions and personality
        # ---------------------------------------------------------------------
        agent = project.agents.create_agent(
            model=azure_foundry_deployment,
            name="IBM Super Cool Agent",
            instructions="You are a helpful assistant that helps users with their questions. "
                        "You are knowledgeable, friendly, and always ready to help. "
                        "Provide clear and helpful responses to user queries.",
        )
        
        # 6. Thread Creation
        # ---------------------------------------------------------------------
        thread = project.agents.threads.create()
        
        # Store the agent and thread in the user session for later use
        cl.user_session.set("agent", agent)
        cl.user_session.set("thread", thread)
        
        print(f"🚀 New chat session started - Agent: {agent.id}, Thread: {thread.id}")
        
    except Exception as e:
        error_message = f"❌ Error initializing agent: {str(e)}"
        await cl.Message(content=error_message, author="System").send()
        print(f"Error in chat start: {e}")

@cl.on_message
async def main(message: cl.Message):
    """
    This function is called every time a user sends a message.
    It processes the message using the AI Agent and returns a response.
    """
    try:
        # Get the agent and thread from the session
        agent = cl.user_session.get("agent")
        thread = cl.user_session.get("thread")
        
        if not agent or not thread:
            await cl.Message(
                content="❌ Session not properly initialized. Please refresh the page.",
                author="System"
            ).send()
            return
        
        # Show a loading message while processing
        thinking_msg = cl.Message(content="🤔 Thinking...", author="IBM Agent")
        await thinking_msg.send()
        
        # 7. Message Creation
        # ---------------------------------------------------------------------
        # Create a new message in the thread with the user's input
        # ---------------------------------------------------------------------
        user_message = project.agents.messages.create(
            thread_id=thread.id, 
            role="user", 
            content=message.content
        )
        
        # 8. Run Creation and Processing
        # ---------------------------------------------------------------------
        # Create and process a run to generate the agent's response
        # ---------------------------------------------------------------------
        run = project.agents.runs.create_and_process(
            thread_id=thread.id, 
            agent_id=agent.id
        )
        
        # 9. Error Handling
        # ---------------------------------------------------------------------
        # Check if the run completed successfully
        # ---------------------------------------------------------------------
        if run.status == "failed":
            error_message = f"❌ Agent run failed: {run.last_error}"
            # Clear the thinking message and add the error
            thinking_msg.content = ""
            await thinking_msg.stream_token(error_message)
            await thinking_msg.update()
            return
        
        # 10. Retrieve and Display Agent Response
        # ---------------------------------------------------------------------
        # Get the agent's response from the thread
        # ---------------------------------------------------------------------
        messages = project.agents.messages.list(
            thread_id=thread.id, 
            order=ListSortOrder.ASCENDING
        )
        
        # Find the agent's response from this run
        agent_response = None
        for msg in messages:
            if msg.run_id == run.id and msg.text_messages and msg.role == "assistant":
                agent_response = msg.text_messages[-1].text.value
                break
        
        if agent_response:
            # Clear the thinking message and stream the actual response
            thinking_msg.content = ""
            await thinking_msg.stream_token(agent_response)
            await thinking_msg.update()
            print(f"✅ Response generated for message: {message.content[:50]}...")
        else:
            # Clear the thinking message and add error message
            error_msg = "❌ Sorry, I couldn't generate a response. Please try again."
            thinking_msg.content = ""
            await thinking_msg.stream_token(error_msg)
            await thinking_msg.update()
        
    except Exception as e:
        error_message = f"❌ Error processing your message: {str(e)}"
        try:
            # Try to update the thinking message if it exists
            thinking_msg.content = ""
            await thinking_msg.stream_token(error_message)
            await thinking_msg.update()
        except:
            # If updating fails, send a new error message
            await cl.Message(content=error_message, author="System").send()
        print(f"Error processing message: {e}")

@cl.on_chat_end
async def end():
    """
    This function is called when the chat session ends.
    It performs cleanup operations and logs the session end.
    """
    try:
        agent = cl.user_session.get("agent")
        thread = cl.user_session.get("thread")
        
        if agent and thread:
            print(f"🔚 Chat session ended - Agent: {agent.id}, Thread: {thread.id}")
        else:
            print("🔚 Chat session ended")
            
        # Note: Azure AI Foundry agents and threads are managed by the service
        # and don't require explicit cleanup. They will be automatically 
        # garbage collected based on the service's retention policies.
        
    except Exception as e:
        print(f"Error during chat end: {e}")

# 11. Running the Application
# ---------------------------------------------------------------------
# To run this application, use the command:
# chainlit run ex2-s2-agentChainlit.py
#
# This will start a web server (usually on http://localhost:8000) where users
# can interact with your AI Agent through a modern chat interface.
#
# Key features of this implementation:
# 1. Interactive web-based chat interface powered by Chainlit
# 2. AI Agent with persistent personality and instructions
# 3. Automatic conversation context management via threads
# 4. Real-time response generation and display
# 5. Session management for multiple concurrent users
# 6. Comprehensive error handling and user feedback
# 7. Integration with Azure AI Foundry's advanced agent capabilities
#
# Advantages over direct chat completions:
# - Automatic context management (no need to manage conversation history)
# - Persistent agent personality and capabilities
# - Built-in error handling and retry logic
# - Enhanced monitoring and debugging features
# - Scalable conversation management
# - Tool integration capabilities for complex tasks (can be extended)
# ---------------------------------------------------------------------
