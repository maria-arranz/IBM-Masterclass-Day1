"""
Simple Chainlit Chat with User Memory (15-min challenge)
--------------------------------------------------------
Basic + Bonus features:
- Asks for user's name when chat starts
- Remembers name throughout conversation
- Uses name in responses and system prompts
- Shows personalized goodbye when chat ends
- BONUS: /info command, message counter, goodbye with stats

Prereqs (env vars):
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_API_VERSION   (e.g. 2024-10-21)
- AZURE_OPENAI_DEPLOYMENT_NAME  (chat model deployment name)

Run with: chainlit run ex1-ch2-solution.py

All messages/logs in English.
"""
import os
import chainlit as cl
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure OpenAI setup
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
)

@cl.on_chat_start
async def start():
    """
    Called when a new chat session starts.
    Ask for user's name and initialize session variables.
    """
    # Send welcome message and ask for name
    await cl.Message(
        content="🤖 Hello! I'm your AI assistant. What's your name?",
        author="Assistant"
    ).send()
    
    # Initialize session variables
    cl.user_session.set("user_name", None)
    cl.user_session.set("waiting_for_name", True)
    cl.user_session.set("message_count", 0)

@cl.on_message
async def main(message: cl.Message):
    """
    Called every time a user sends a message.
    Handle name collection and regular chat.
    """
    waiting_for_name = cl.user_session.get("waiting_for_name", False)
    
    # First, check if we're waiting for the user's name
    if waiting_for_name:
        user_name = message.content.strip()
        cl.user_session.set("user_name", user_name)
        cl.user_session.set("waiting_for_name", False)
        
        await cl.Message(
            content=f"Nice to meet you, {user_name}! How can I help you today? (Type /info for your stats)",
            author="Assistant"
        ).send()
        return
    
    # Get stored user information
    user_name = cl.user_session.get("user_name", "friend")
    message_count = cl.user_session.get("message_count", 0) + 1
    cl.user_session.set("message_count", message_count)
    
    # Handle special commands
    if message.content.strip().lower() == "/info":
        await cl.Message(
            content=f"📊 User: {user_name} | Messages sent: {message_count}",
            author="System"
        ).send()
        return
    
    # Build personalized system prompt
    system_message = f"You are a helpful assistant talking to {user_name}. Keep answers friendly and concise."
    
    # Prepare messages for Azure OpenAI
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": message.content}
    ]
    
    # Show loading message
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        # Call Azure OpenAI with streaming
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=messages,
            temperature=0.7,
            max_completion_tokens=1000,
            stream=True
        )
        
        # Stream the response
        content = ""
        for chunk in response:
            if chunk.choices and len(chunk.choices) > 0:
                if chunk.choices[0].delta.content is not None:
                    content += chunk.choices[0].delta.content
                    await msg.stream_token(chunk.choices[0].delta.content)
        
        # Finalize the streamed message
        await msg.update()
        
    except Exception as e:
        # Handle errors gracefully
        error_message = f"❌ Sorry {user_name}, I encountered an error: {str(e)}"
        error_msg = cl.Message(content=error_message, author="System")
        await error_msg.send()

@cl.on_chat_end
async def end():
    """
    Called when the chat session ends.
    Show personalized goodbye with stats.
    """
    user_name = cl.user_session.get("user_name", "friend")
    message_count = cl.user_session.get("message_count", 0)
    
    print(f"Chat ended - User: {user_name}, Messages: {message_count}")
    
    # Note: on_chat_end doesn't support sending messages to the user
    # but we can log the session info for debugging/analytics
