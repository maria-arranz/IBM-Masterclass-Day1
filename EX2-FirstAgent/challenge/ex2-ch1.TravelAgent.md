# 🤖 Challenge: AI Agent Travel Companion with Chainlit

<div align="center">

![Challenge](https://img.shields.io/badge/Challenge-EX2-blue?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Difficulty-Beginner-green?style=for-the-badge)
![Time](https://img.shields.io/badge/Time-15%20minutes-orange?style=for-the-badge)
![Agent](https://img.shields.io/badge/AI-Agent%20Powered-purple?style=for-the-badge)

**Create a personalized travel companion AI agent with memory and conversation management!**

</div>

---

## 🎯 **Objective**

Transform the existing Azure AI Foundry agent examples into a **specialized travel companion** that helps users plan their trips. Combine the power of AI Agents with Chainlit's modern web interface to create an engaging travel planning experience!

## ✨ **What You'll Learn**

<table>
<tr>
<td>

### 🤖 **AI Agent Skills**
- Customizing agent instructions for specific domains
- Managing conversation threads and context
- Agent-based architecture advantages

</td>
<td>

### 🌐 **Integration Concepts**
- Combining Azure AI Foundry with web interfaces
- Session management with agent persistence
- Professional travel application design

</td>
</tr>
</table>

---

## 📝 **Challenge Description**

Based on the examples in this folder (`ex2-s1-agentaiservice.py` and `ex2-s2-agentChainlit.py`), create a specialized travel companion agent that:

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin: 15px 0; color: white;">

### 🎯 **Your Mission**

1. **✈️ Specializes in travel advice** with customized agent instructions
2. **🙋‍♂️ Asks for the user's destination** when the chat starts
3. **🧠 Remembers trip details** throughout the conversation using agent threads
4. **🎨 Uses travel-themed interface** with emojis and personalized messages
5. **👋 Provides trip summary** and helpful resources when ending

</div>

---

## 📋 **Technical Requirements**

### 🥇 **Basic Level (10-15 minutes)** ✅ MAIN GOAL

<div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; margin: 10px 0;">

**Perfect for learning domain-specific AI agent development!**

- [ ] ✅ Create an agent with **travel-focused instructions**
- [ ] ✅ Ask for the user's **travel destination** at chat start
- [ ] ✅ Store destination in **session state** for context
- [ ] ✅ Include destination in the **agent's system prompt**
- [ ] ✅ Use travel-themed **emojis and messages** throughout
- [ ] ✅ Show **travel tips** in the welcome message

</div>

### 🌟 **Advanced Level (Extra 5 minutes for fast finishers)** 🎖️ BONUS

<div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 10px 0;">

**For those who want to build a more sophisticated travel assistant!**

- [ ] 🔥 Ask for **travel dates and budget** in addition to destination
- [ ] 🔥 Add a `/trip-info` command to display stored trip details
- [ ] 🔥 Count questions asked and show in goodbye message
- [ ] 🔥 Provide **city-specific resources** (websites, local tips) on exit

</div>

---

## 💡 **Getting Started Hints**

### 🟢 **Basic Level Implementation**

<details>
<summary>🔍 <strong>Click to see key changes needed</strong></summary>

```python
# Key modifications to make in your Chainlit + Agent app:

# 1. Update agent instructions (in @cl.on_chat_start)
agent = project.agents.create_agent(
    model=azure_foundry_deployment,
    name="Travel Companion Agent",
    instructions="""You are an expert travel companion and advisor. 
    You help users plan amazing trips by providing personalized recommendations for:
    - Attractions and activities
    - Local restaurants and cuisine
    - Transportation options
    - Cultural tips and etiquette
    - Budget-friendly suggestions
    - Hidden gems and local favorites
    
    Always be enthusiastic, helpful, and provide specific actionable advice.
    Use the user's destination to tailor all your recommendations.""",
)

# 2. Ask for destination and store it
destination_response = await cl.AskUserMessage(
    content="🌍 Where are you planning to travel? Please enter your destination:",
    timeout=60
).send()

if destination_response:
    # Handle Chainlit response format (may be dict or object)
    if isinstance(destination_response, dict):
        destination = destination_response.get("output", "Unknown destination")
    else:
        destination = destination_response.content
    
    cl.user_session.set("destination", destination)
    
    # Welcome message with destination
    await cl.Message(
        content=f"✈️ Fantastic! I'm excited to help you plan your trip to **{destination}**! 🎉\n\n"
               f"🗺️ I can help you with:\n"
               f"• 🏛️ Must-see attractions and activities\n"
               f"• 🍽️ Local restaurants and food recommendations\n" 
               f"• 🚌 Transportation and getting around\n"
               f"• 💰 Budget-friendly tips and deals\n"
               f"• 🎭 Cultural insights and local customs\n\n"
               f"What would you like to know about {destination}?",
        author="Travel Agent"
    ).send()

# 3. Include destination in agent instructions
# Update your agent creation to include the destination in the instructions
```

</details>

### 🌟 **Advanced Level Enhancements**

<details>
<summary>🔍 <strong>Click to see bonus features code</strong></summary>

```python
# Advanced features to add:

# 1. Collect more trip details
travel_dates_response = await cl.AskUserMessage(
    content="📅 When are you planning to travel? (e.g., 'March 2024' or 'Summer')",
    timeout=60
).send()

budget_response = await cl.AskUserMessage(
    content="💰 What's your approximate budget range? (e.g., 'Budget-friendly', '$1000-2000', 'Luxury')",
    timeout=60
).send()

# Store all details - handle response format
travel_dates = travel_dates_response.get("output", "Not specified") if travel_dates_response else "Not specified"
budget = budget_response.get("output", "Not specified") if budget_response else "Not specified"

cl.user_session.set("travel_dates", travel_dates)
cl.user_session.set("budget", budget)

# 2. Add trip info command
@cl.on_message
async def main(message: cl.Message):
    # Check for commands first
    if message.content.lower() == "/trip-info":
        destination = cl.user_session.get("destination", "Not set")
        dates = cl.user_session.get("travel_dates", "Not set")
        budget = cl.user_session.get("budget", "Not set")
        question_count = cl.user_session.get("question_count", 0)
        
        await cl.Message(
            content=f"🎒 **Your Trip Details:**\n\n"
                   f"📍 **Destination:** {destination}\n"
                   f"📅 **Travel Dates:** {dates}\n"
                   f"💰 **Budget:** {budget}\n"
                   f"❓ **Questions Asked:** {question_count}",
            author="Travel Agent"
        ).send()
        return

# 3. Count questions and enhance goodbye
question_count = cl.user_session.get("question_count", 0) + 1
cl.user_session.set("question_count", question_count)
```

</details>

---

## 🔧 **Key Changes from Base Examples**

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0;">

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff;">

**🎯 Specialized Agent**
- Travel-focused system instructions
- Domain-specific knowledge and tone

</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">

**📍 Destination Context**
- Ask for travel destination
- Store in session for persistence

</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #dc3545;">

**🎨 Travel Theme**
- Travel emojis and terminology
- Enthusiastic and helpful tone

</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">

**💬 Enhanced UX**
- Welcome tips and guidance
- Structured travel categories

</div>

</div>

---

## ✅ **Success Criteria**

<div style="background: #d1ecf1; padding: 20px; border-radius: 10px; border-left: 4px solid #0c5460;">

**Your travel companion should achieve all of these:**

- ✅ Agent **specializes in travel advice** with appropriate instructions
- ✅ **Asks for destination** when chat starts using `cl.AskUserMessage`
- ✅ **Remembers destination** throughout the conversation
- ✅ Uses **travel-themed interface** with emojis and friendly tone
- ✅ Provides **structured travel categories** in welcome message
- ✅ Agent responses are **context-aware** of the destination

</div>

---

## 🌍 **Example Conversation Flow**

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">

```
🤖 Travel Agent: 🌍 Where are you planning to travel?
👤 User: Tokyo, Japan

✈️ Travel Agent: Fantastic! I'm excited to help you plan your trip to Tokyo, Japan! 🎉

🗺️ I can help you with:
• 🏛️ Must-see attractions (Senso-ji Temple, Tokyo Skytree...)
• 🍽️ Local restaurants and food (ramen shops, sushi spots...)
• 🚌 Transportation (JR Pass, metro system...)
• 💰 Budget-friendly tips and deals
• 🎭 Cultural insights (bowing etiquette, shoe removal...)

What would you like to know about Tokyo?

👤 User: What are the must-see neighborhoods?
🤖 Travel Agent: For Tokyo, I highly recommend these neighborhoods:
[Agent provides Tokyo-specific recommendations...]
```

</div>

---

## ⏱️ **Time Estimation**

<div align="center">

| Level | Time | What You'll Build |
|-------|------|-------------------|
| 🟢 **Basic** | 10-15 minutes | Travel-focused agent with destination memory |
| 🟡 **Advanced** | +5 minutes | Enhanced with trip details and commands |

</div>

---

## 📦 **Deliverables**

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; margin: 15px 0;">

### 🎯 **What to Submit**

1. **📄 Modified Python file** → Save as `ex2-travel-companion-YOURNAME.py`
2. **🧪 Quick test** → Make sure the travel flow works end-to-end!
3. **🌍 Try different destinations** → Test with various travel locations

*Example: If your name is Sarah, save as `ex2-travel-companion-sarah.py`*

</div>

---

## 🚀 **Getting Started**

1. **📁 Start with** `ex2-s2-agentChainlit.py` as your base
2. **🎯 Focus first** on the basic requirements (travel agent instructions + destination)
3. **✨ Add polish** with emojis and travel-themed messages
4. **🎖️ Add bonuses** if you finish early

---

<div align="center">

## 🎉 **Ready to Build Your AI Travel Companion?**

*Transform a generic agent into a specialized travel advisor that users will love to interact with!*

**✈️ Let's help people plan amazing trips with AI! 🌍**

---

💡 **Pro Tip:** Think about what questions travelers always ask, and design your agent to proactively address those topics!

</div>
