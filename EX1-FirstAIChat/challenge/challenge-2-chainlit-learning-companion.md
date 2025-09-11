# 🎯 Challenge 2: Simple Chainlit Chat with User Memory

## Objective
Transform the basic Chainlit example into a chat that remembers the user's name and shows a simple welcome/goodbye experience.

## What You'll Learn
- Chainlit session management basics
- Simple user state storage
- Chainlit event handlers (start, message, end)
- Basic personalization in web chat interfaces

## Challenge Description
Based on the example `ex1-s2-chainlit.py`, modify the code to create a Chainlit chat that:

1. **Asks for the user's name** when the chat starts
2. **Remembers the name** throughout the conversation
3. **Uses the name** in responses and system prompts
4. **Shows a personalized goodbye** when the chat ends

## Technical Requirements

### Basic Level (10-15 minutes) ✅ MAIN GOAL
- [ ] Ask for user's name in the `@cl.on_chat_start` function
- [ ] Store the name in `cl.user_session`
- [ ] Use the stored name in the system prompt
- [ ] Personalize responses with the user's name
- [ ] Show a goodbye message with the user's name

### Advanced Level (Extra 5 minutes for fast finishers) 🌟 BONUS
- [ ] Count the number of messages sent by the user
- [ ] Add a simple `/info` command that shows user info
- [ ] Show message count in the goodbye

## Getting Started Hints (Basic Level)

```python
# Key changes to make in your Chainlit app:

@cl.on_chat_start
async def start():
    """Ask for user's name and store it"""
    # Send welcome message and ask for name
    await cl.Message(
        content="🤖 Hello! I'm your AI assistant. What's your name?",
        author="Assistant"
    ).send()
    
    # Initialize session variables
    cl.user_session.set("user_name", None)
    cl.user_session.set("waiting_for_name", True)

@cl.on_message
async def main(message: cl.Message):
    """Handle messages - check if we need the name first"""
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
    
    # Get stored name for regular chat
    user_name = cl.user_session.get("user_name", "friend")
    
    # Build personalized system prompt
    system_message = f"You are a helpful assistant talking to {user_name}. Keep answers friendly and concise."
    
    # Your existing Azure OpenAI code here...
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": message.content}
    ]
    
    # ... rest of your response handling
```

## Getting Started Hints (Advanced Level)

```python
# Add these for bonus features:

# In on_chat_start, also initialize:
cl.user_session.set("message_count", 0)

# In on_message, increment counter:
message_count = cl.user_session.get("message_count", 0) + 1
cl.user_session.set("message_count", message_count)

# Add /info command handling:
if message.content.strip().lower() == "/info":
    user_name = cl.user_session.get("user_name", "Unknown")
    message_count = cl.user_session.get("message_count", 0)
    
    await cl.Message(
        content=f"📊 User: {user_name} | Messages sent: {message_count}",
        author="System"
    ).send()
    return

@cl.on_chat_end
async def end():
    """Show personalized goodbye with stats"""
    user_name = cl.user_session.get("user_name", "friend")
    message_count = cl.user_session.get("message_count", 0)
    
    print(f"Chat ended - User: {user_name}, Messages: {message_count}")
```

## Key Changes from Original Example
1. **Ask for name** in `on_chat_start`
2. **Store name** in session using `cl.user_session.set()`
3. **Check if waiting for name** before processing regular messages
4. **Personalize system prompt** with stored name
5. **Add goodbye logic** in `on_chat_end`

## Success Criteria
- ✅ Chat asks for user's name at start
- ✅ Responses are personalized with the user's name
- ✅ Name is remembered throughout the conversation
- ✅ Goodbye message includes the user's name
- ✅ Chat works smoothly in the web interface

## Time Estimation
- **Basic Level**: 10-15 minutes
- **With Bonus Features**: 15-20 minutes

## How to Test
1. Save your file as `ex1-ch2-YOURNAME.py`
2. Run: `chainlit run ex1-ch2-YOURNAME.py`
3. Open the web interface (usually http://localhost:8000)
4. Test the name flow and personalization

## Deliverables
1. Modified Chainlit file (`ex1-ch2-YOURNAME.py`)
2. Quick test in the web interface!

This shows you the power of session management in web-based AI chats! 🚀
