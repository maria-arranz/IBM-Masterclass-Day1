# 🎯 Challenge 2: Simple Chainlit Chat with User Memory

<div align="center">

![Challenge 2](https://img.shields.io/badge/Challenge-2-purple?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Difficulty-Beginner-green?style=for-the-badge)
![Time](https://img.shields.io/badge/Time-15%20minutes-orange?style=for-the-badge)
![Web](https://img.shields.io/badge/Interface-Web%20Based-blue?style=for-the-badge)

**Transform basic Chainlit into a personalized web chat experience!**

</div>

---

## 🎯 **Objective**

Transform the `ex1-s2-chainlit.py` example into a **smarter web chat** that remembers users and provides a personalized experience. Learn the fundamentals of session management in modern AI web interfaces!

## ✨ **What You'll Learn**

<table>
<tr>
<td>

### 🌐 **Web AI Skills**
- Chainlit session management basics
- Simple user state storage  
- Event-driven chat architecture

</td>
<td>

### 🧠 **AI UX Concepts**
- Personalized welcome/goodbye flows
- Web-based conversation state
- Professional chat interface design

</td>
</tr>
</table>

---

## 📝 **Challenge Description**

Based on the example `ex1-s2-chainlit.py`, modify the code to create a Chainlit chat that:

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 10px; margin: 15px 0; color: white;">

### 🎯 **Your Mission**

1. **🙋‍♂️ Asks for the user's name** when the chat starts
2. **🧠 Remembers the name** throughout the entire conversation
3. **👤 Uses the name** in responses and system prompts  
4. **👋 Shows a personalized goodbye** when the chat ends

</div>

---

## 📋 **Technical Requirements**

### 🥇 **Basic Level (10-15 minutes)** ✅ MAIN GOAL

<div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; margin: 10px 0;">

**Perfect for learning web-based AI chat fundamentals!**

- [ ] ✅ Ask for user's name in the `@cl.on_chat_start` function
- [ ] ✅ Store the name in `cl.user_session` for persistence
- [ ] ✅ Use the stored name in the system prompt
- [ ] ✅ Personalize responses with the user's name
- [ ] ✅ Show a goodbye message with the user's name

</div>

### 🌟 **Advanced Level (Extra 5 minutes for fast finishers)** � BONUS

<div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 10px 0;">

**For those who want to add some extra polish!**

- [ ] 🔥 Count the number of messages sent by the user
- [ ] 🔥 Add a simple `/info` command that shows user stats
- [ ] 🔥 Show message count in the goodbye message

</div>

---

## 💡 **Getting Started Hints**

### 🟢 **Basic Level Implementation**

<details>
<summary>🔍 <strong>Click to see key code changes needed</strong></summary>

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

</details>

### 🌟 **Advanced Level Enhancements**

<details>
<summary>🔍 <strong>Click to see bonus features code</strong></summary>

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

</details>

---

## 🔧 **Key Changes from Original Example**

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0;">

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff;">

**🎬 Smart Start Flow**
- Ask for name in `on_chat_start`
- Handle name collection before regular chat

</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">

**🧠 Session Memory**
- Store name with `cl.user_session.set()`
- Retrieve name with `cl.user_session.get()`

</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #dc3545;">

**👤 Personalization**
- Use name in system prompts
- Include name in responses

</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">

**👋 Graceful Goodbye**
- Implement `on_chat_end` handler
- Show personalized farewell

</div>

</div>

---

## ✅ **Success Criteria**

<div style="background: #d1ecf1; padding: 20px; border-radius: 10px; border-left: 4px solid #0c5460;">

**Your Chainlit app should achieve all of these:**

- ✅ Chat **asks for user's name** at startup
- ✅ Responses are **personalized** with the user's name
- ✅ Name is **remembered** throughout the entire conversation
- ✅ **Goodbye message** includes the user's name  
- ✅ Chat works **smoothly** in the web interface

</div>

---

## ⏱️ **Time Estimation**

<div align="center">

| Level | Time | What You'll Build |
|-------|------|-------------------|
| 🟢 **Basic** | 10-15 minutes | Personalized web chat with memory |
| 🟡 **Advanced** | +5 minutes | Enhanced with stats and commands |

</div>

---

## 🧪 **How to Test Your Solution**

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; margin: 15px 0;">

### 🔬 **Testing Steps**

1. **💾 Save** your file as `ex1-ch2-YOURNAME.py`
2. **🚀 Run** the command: `chainlit run ex1-ch2-YOURNAME.py`
3. **🌐 Open** the web interface (usually http://localhost:8000)
4. **✅ Test** the name flow and personalization
5. **🎉 Celebrate** when it works!

</div>

---

## 📦 **Deliverables**

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 10px; color: white; margin: 15px 0;">

### 🎯 **What to Submit**

1. **📄 Modified Chainlit file** → Save as `ex1-ch2-YOURNAME.py`
2. **🧪 Quick web test** → Make sure it works in the browser!

*Example: If your name is Alex, save as `ex1-ch2-alex.py`*

</div>

---

<div align="center">

## 🎉 **Ready to Build Your First Smart Web Chat?**

*This shows you the power of session management in web-based AI chats!*

**🚀 Let's make that basic Chainlit example remember and personalize! 🚀**

---

💡 **Pro Tip:** Start with the basic name flow, then add bonus features if you have time!

⚡ **Quick Start:** Copy the example code, add the name logic, and test in your browser!

</div>
