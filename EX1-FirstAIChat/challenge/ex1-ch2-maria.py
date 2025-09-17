# 0. Import necessary libraries and set up environment variables
import os
import chainlit as cl
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

azureServices_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azureServices_key = os.getenv("AZURE_OPENAI_API_KEY")
azureServices_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
azureServices_apiVersion = os.getenv("AZURE_OPENAI_API_VERSION")


client = AzureOpenAI(
    azure_endpoint=azureServices_endpoint,
    api_version=azureServices_apiVersion,
    api_key=azureServices_key,
    azure_deployment=azureServices_deployment
)

# 2. ChainLit Event Handlers for Interactive Chat
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
    It's useful for initializing the conversation and setting up any session-specific data.
    """
    # Send a welcome message to the user
    await cl.Message(
        content="🤖 Hello! I'm your AI assistant. What's your name?",
        author="Assistant"
    ).send()
    
    # Store the system message in the user session for context
    cl.user_session.set("system_message", "You are a helpful assistant.")
    cl.user_session.set("conversation_history", [])
    cl.user_session.set("user_name", None)
    cl.user_session.set("waiting_for_name", True)

@cl.on_message
async def main(message: cl.Message):

    waiting_for_name = cl.user_session.get("waiting_for_name", False)

    if waiting_for_name:
        # Store the name and send confirmation
        user_name = message.content.strip()
        cl.user_session.set("user_name", user_name)
        cl.user_session.set("waiting_for_name", False)
        
        await cl.Message(
            content=f"Nice to meet you, {user_name}! How can I help you today?",
            author="Assistant"
        ).send()
        return
    
    user_name = cl.user_session.get("user_name", "friend")

    system_message = f"You are a helpful assistant talking to {user_name}. Keep answers friendly and concise."

    conversation_history = cl.user_session.get("conversation_history", [])
    
    # Add the new user message to the conversation history
    conversation_history.append({
        "role": "user",
        "content": message.content
    })
    
    # Build the messages array for the API call
    messages = [
        {
            "role": "system",
            "content": system_message
        }
    ] + conversation_history
    
    # Show a loading message while processing
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        # 3. Creating a Chat Completion Request using the client
        # When you send a request to Azure OpenAI, you need to provide some information so the service knows 
        # which model to use and how to answer. 
        # ---------------------------------------------------------------------
        
        response = client.chat.completions.create(
            model=azureServices_deployment,
            max_completion_tokens=1500,
            temperature=1.0,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            messages=messages,
            stream=True  # Enable streaming for better user experience
        )
        
        # 4. Stream the response and update the message in real-time
        # ---------------------------------------------------------------------
        # Streaming provides a better user experience by showing the response as it's generated
        # instead of waiting for the complete response.
        # ---------------------------------------------------------------------
        content = ""
        for chunk in response:
            # Check if the chunk has choices and delta content
            if chunk.choices and len(chunk.choices) > 0:
                if chunk.choices[0].delta.content is not None:
                    content += chunk.choices[0].delta.content
                    await msg.stream_token(chunk.choices[0].delta.content)
        
        # Finalize the streamed message
        await msg.update()
        
        # Add the assistant's response to the conversation history
        conversation_history.append({
            "role": "assistant",
            "content": content
        })
        
        # Update the conversation history in the session
        cl.user_session.set("conversation_history", conversation_history)
        
        # 5. Display token usage information (optional)
        # ---------------------------------------------------------------------
        # Note: When using streaming, token usage information might not be available
        # in each chunk. You can make a separate non-streaming call to get accurate
        # token counts if needed for monitoring purposes.
        # ---------------------------------------------------------------------
        
    except Exception as e:
        # Handle any errors that might occur during the API call
        error_message = f"❌ Error processing your message: {str(e)}"
        # Create a new message for the error instead of updating the existing one
        error_msg = cl.Message(content=error_message, author="System")
        await error_msg.send()

@cl.on_chat_end
async def end():
    """
    This function is called when the chat session ends.
    It's useful for cleanup operations or logging.
    """

    user_name = cl.user_session.get("user_name", "friend")
    print(f"Chat session ended. Goodbye {user_name}!")

# 6. Additional ChainLit Configuration (Optional)
# ---------------------------------------------------------------------
# You can customize the ChainLit interface by adding configuration
# This would typically go in a chainlit.md file or can be set programmatically
# ---------------------------------------------------------------------

# To run this application, use the command:
# chainlit run ex1-s2-chainlit.py
#
# This will start a web server (usually on http://localhost:8000) where users
# can interact with your AI assistant through a modern chat interface.
#
# Key differences from the original script:
# 1. Interactive web-based chat interface instead of single Q&A
# 2. Conversation history maintained across messages
# 3. Real-time streaming of responses for better UX
# 4. Session management for multiple concurrent users
# 5. Event-driven architecture with decorators
# 6. Better error handling and user feedback
