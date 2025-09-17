# 🛠️ Challenge 3: Multi-Function Agent Assistant

<div align="center">

![Challenge 3](https://img.shields.io/badge/Challenge-3-blue?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Difficulty-Beginner-green?style=for-the-badge)
![Time](https://img.shields.io/badge/Time-20%20minutes-orange?style=for-the-badge)

**Build an AI agent with multiple custom functions for real-world tasks!**

</div>

---

## 🎯 **Objective**

Transform the `ex3-s1-FunctionCalling.py` example into a comprehensive personal assistant agent with multiple custom functions. Learn how to design and implement function calling to create powerful AI tools that can perform various tasks!

## ✨ **What You'll Learn**

<table>
<tr>
<td>

### 🔄 **Core Skills**
- Designing multiple custom functions for AI agents
- Function parameter handling and validation
- Creating practical utility functions
- Managing multiple function calls in one conversation

</td>
<td>

### 🧠 **AI Concepts**  
- Function calling architecture
- Tool definition and registration
- Multi-function agent workflows
- Practical AI assistant design patterns

</td>
</tr>
</table>

---

## 📝 **Challenge Description**

Based on the example `ex3-s1-FunctionCalling.py`, create a personal assistant agent that can handle multiple types of requests through custom functions:

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin: 15px 0; color: white;">

### 🎯 **Your Mission**

1. **🌤️ Extend the weather function** to support multiple cities and provide detailed information
2. **⏰ Add a time/date function** that can handle different time zones and formats
3. **🔐 Create a password generator function** for secure password creation
4. **📝 Build a task management function** to add, list, and complete tasks
5. **🎲 Add a fun random function** like jokes, facts, or number generation

**🌟 Goal**: Create an agent that can handle diverse requests in a single conversation!

</div>

---

## 📋 **Technical Requirements**

### 🥇 **Basic Level (15-20 minutes)** ✅ MAIN GOAL

<div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; margin: 10px 0;">

**Perfect for learning function calling fundamentals!**

- [ ] ✅ **Enhanced Weather Function**: Support multiple cities with detailed info (temperature, conditions, humidity)
- [ ] ✅ **Time Function**: Get current time with timezone support (at least 3 time zones)
- [ ] ✅ **Password Generator Function**: Create secure passwords with customizable options
- [ ] ✅ **Test all functions**: Create a conversation that uses each function at least once

</div>

### 🌟 **Advanced Level (Extra 10 minutes for fast finishers)** ⭐ BONUS

<div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 10px 0;">

**For those who finish early and want extra functionality!**

- [ ] 🔥 **Task Manager**: Add, list, mark complete, and delete tasks
- [ ] 🔥 **Random Content**: Generate jokes, random facts, or lucky numbers
- [ ] 🔥 **Conversation Flow**: Handle multiple requests in one message
- [ ] 🔥 **Error Handling**: Gracefully handle invalid inputs with helpful messages

</div>

---

## 💡 **Getting Started Hints**

### 🟢 **Basic Level Implementation**

<details>
<summary>🔍 <strong>Click to see function templates</strong></summary>

```python
# Enhanced Weather Function
def fetch_weather(location: str, include_forecast: bool = False) -> str:
    """
    Fetches detailed weather information for the specified location.
    
    :param location: The location to fetch weather for
    :param include_forecast: Whether to include a 3-day forecast
    :return: Weather information as a JSON string
    """
    # Your implementation here
    pass

# Time Function  
def get_current_time(timezone: str = "UTC") -> str:
    """
    Gets the current time in the specified timezone.
    
    :param timezone: Timezone (UTC, EST, PST, CET, etc.)
    :return: Current time as a JSON string
    """
    # Your implementation here
    pass

# Calculator Function
def generate_password(length: int = 12, include_symbols: bool = True) -> str:
    """
    Generates a secure random password.
    
    :param length: Length of the password (8-50 characters)
    :param include_symbols: Whether to include special symbols (!@#$%^&*)
    :return: Generated password as a JSON string
    """
    # Your implementation here
    pass
```

</details>

<details>
<summary>🎯 <strong>Sample Data Ideas</strong></summary>

```python
# Weather Data
weather_database = {
    "New York": {"temp": "18°C", "condition": "Cloudy", "humidity": "65%"},
    "London": {"temp": "12°C", "condition": "Rainy", "humidity": "80%"},
    "Tokyo": {"temp": "22°C", "condition": "Sunny", "humidity": "55%"},
    "Sydney": {"temp": "25°C", "condition": "Partly Cloudy", "humidity": "60%"},
    "Barcelona": {"temp": "25°C", "condition": "Sunny", "humidity": "45%"}
}

# Timezone Mappings
timezones = {
    "EST": -5, "PST": -8, "CET": 1, "JST": 9, "AEST": 10, "UTC": 0
}

# Password Generation Characters
password_chars = {
    "uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "lowercase": "abcdefghijklmnopqrstuvwxyz", 
    "numbers": "0123456789",
    "symbols": "!@#$%^&*()_+-=[]{}|;:,.<>?"
}
```

</details>

<details>
<summary>🚀 <strong>Test Questions to Try</strong></summary>

**Mix these requests in your conversation:**

- "What's the weather like in Tokyo and include the forecast?"
- "What time is it in New York right now?"
- "Generate a secure password with 16 characters including symbols"
- "Can you tell me the weather in London and create a password for me?"
- "I need a simple password without symbols, make it 10 characters long"

</details>

---

### 🟡 **Advanced Level Implementation**

<details>
<summary>⚡ <strong>Advanced Function Ideas</strong></summary>

```python
# Task Manager Function
def manage_tasks(action: str, task: str = "", task_id: int = 0) -> str:
    """
    Manages a simple task list.
    
    :param action: Action to perform (add, list, complete, delete)
    :param task: Task description (for add action)
    :param task_id: Task ID (for complete/delete actions)
    :return: Task management result as JSON
    """
    # Your implementation here
    pass

# Random Content Function
def get_random_content(content_type: str) -> str:
    """
    Generates random content like jokes, facts, or numbers.
    
    :param content_type: Type of content (joke, fact, number)
    :return: Random content as JSON
    """
    # Your implementation here
    pass
```

</details>

<details>
<summary>🔥 <strong>Advanced Test Scenarios</strong></summary>

**Try these complex interactions:**

- "Add a task to 'Buy groceries', then tell me what time it is in London"
- "Generate a strong password and create a random joke"
- "What's the weather in Barcelona, add a task 'Check weather app', and give me a random fact"
- "List all my tasks and create a password for my new account"

</details>

---

## 🔧 **Implementation Guide**

### **Step 1: Set Up Your Functions**
Start with the basic weather function from the example and gradually add new functions one by one.

### **Step 2: Test Each Function**
Before adding multiple functions, make sure each one works individually.

### **Step 3: Register All Functions**
Add all your functions to the `user_functions` set:
```python
user_functions = {fetch_weather, get_current_time, generate_password, manage_tasks, get_random_content}
```

### **Step 4: Handle Function Calls**
In the `requires_action` section, add handlers for each function:
```python
if tool_call.function.name == "your_function_name":
    # Parse arguments and call your function
    output = your_function(args)
    tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
```

---

## 🎯 **Success Criteria**

### ✅ **You'll know you've succeeded when:**

**Basic Level:**
- Your agent can answer weather questions for multiple cities
- Time queries work for different timezones  
- Password generator creates secure passwords with options
- All functions return properly formatted JSON responses

**Advanced Level:**
- Task management works smoothly
- Random content adds personality to your agent
- Your agent handles complex multi-function requests
- Error handling provides helpful feedback

---

## 🆘 **Common Issues & Solutions**

<details>
<summary>❗ <strong>Function Not Being Called</strong></summary>

**Problem**: Agent doesn't call your custom function

**Solutions**:
- Check your function docstring format
- Ensure function is in the `user_functions` set
- Verify the function name matches in the handler
- Make sure parameters are correctly typed

</details>

<details>
<summary>❗ <strong>JSON Parsing Errors</strong></summary>

**Problem**: Function returns cause parsing errors

**Solutions**:
- Always return valid JSON strings
- Use `json.dumps()` to ensure proper formatting
- Handle edge cases (empty results, invalid inputs)

</details>

<details>
<summary>❗ <strong>Function Arguments Not Working</strong></summary>

**Problem**: Function receives wrong or missing arguments

**Solutions**:
- Check parameter names in docstring match function signature
- Use proper type hints
- Parse arguments from `tool_call.function.arguments` if needed

</details>

---

## 🏆 **Bonus Challenges**

If you finish everything and want more:

1. **🌍 Language Support**: Make your weather function support cities in different languages
2. **📊 Data Persistence**: Make tasks persist between conversations (hint: use a file)
3. **🎨 Rich Formatting**: Add emojis and formatting to make responses more engaging
4. **🔒 Input Validation**: Add comprehensive error checking for all function inputs

---

## 📚 **Key Learning Outcomes**

By completing this challenge, you'll understand:

- How to design multiple interconnected functions for AI agents
- Best practices for function documentation and parameter handling
- How to create practical, real-world AI assistants
- The power of function calling for extending AI capabilities

**🎉 Ready to build your multi-function AI assistant? Let's get coding!**

---

<div align="center">

**💡 Remember**: Start simple and add complexity gradually. The goal is to learn function calling patterns, not to build a perfect application!

</div>