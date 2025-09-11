# 🚀 Challenge 1: Interactive Chat Loop with Azure OpenAI

<div align="center">

![Challenge 1](https://img.shields.io/badge/Challenge-1-blue?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Difficulty-Beginner-green?style=for-the-badge)
![Time](https://img.shields.io/badge/Time-15%20minutes-orange?style=for-the-badge)

**Transform a single-question example into an interactive conversation!**

</div>

---

## 🎯 **Objective**

Transform the static `ex1-s1-aoai.py` example into a dynamic, interactive chat where users can have **multiple conversations** with the AI assistant. Learn the fundamentals of conversation loops and personalization!

## ✨ **What You'll Learn**

<table>
<tr>
<td>

### 🔄 **Core Skills**
- Converting single-request code into interactive loops
- Basic user input handling with Python
- Simple conversation flow management

</td>
<td>

### 🧠 **AI Concepts**  
- Personalizing system prompts dynamically
- Managing conversation state
- Practical Azure OpenAI implementation

</td>
</tr>
</table>

---

## 📝 **Challenge Description**

Based on the example `ex1-s1-aoai.py`, modify the code to create an interactive chat that:

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin: 15px 0; color: white;">

### 🎯 **Your Mission**

1. **🙋‍♂️ Asks the user their name** when starting
2. **🔄 Keeps asking for new questions** until the user types "quit"  
3. **👤 Uses the user's name** in the system prompt to personalize responses
4. **📊 Shows token usage** after each response

</div>

---

## 📋 **Technical Requirements**

### 🥇 **Basic Level (10-15 minutes)** ✅ MAIN GOAL

<div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; margin: 10px 0;">

**Perfect for getting started with interactive AI chats!**

- [ ] ✅ Create a simple `while` loop for continuous conversation
- [ ] ✅ Ask for user's name at the beginning  
- [ ] ✅ Include the user's name in the system prompt
- [ ] ✅ Allow user to type "quit" to exit gracefully
- [ ] ✅ Keep showing token usage after each response

</div>

### 🌟 **Advanced Level (Extra 5 minutes for fast finishers)** � BONUS

<div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 10px 0;">

**For those who finish early and want extra credit!**

- [ ] 🔥 Keep track of how many questions the user has asked
- [ ] 🔥 Add a goodbye message with conversation summary when quitting

</div>

---

## 💡 **Getting Started Hints**

### 🟢 **Basic Level Implementation**

<details>
<summary>🔍 <strong>Click to see starter code structure</strong></summary>

```python
# Simple structure to get you started
## use the code from ex1-s1-aoai.py as a base and later... just to inspire you

print("🤖 Welcome to your AI Assistant! (type /help for options)")
user_name = input("What's your name? ").strip() or "friend"

def system_prompt(name: str) -> str:
    return (
        f"You are a helpful assistant. You are talking to {name}. "
        "Keep answers clear and concise."
    )

print(f"Hi {user_name}! Ask me anything. Type 'quit' to exit.")

while True:
    user_input = input(f"\n{user_name}, what would you like to ask? ").strip()

    if not user_input:
        continue

    if user_input.lower() == "quit":
        print("\n[info] Exiting...")
        print(f"Goodbye {user_name}!")
        break

    # Build a minimal message list (single-turn style) — simple for the 15-min challenge
    messages = [
        {"role": "system", "content": system_prompt(user_name)},
        {"role": "user", "content": user_input},
    ]

    try:
        # here you should call the Azure OpenAI client (response = ...)
        # Following some additional hints below...

        answer = resp.choices[0].message.content or "(no content)"
        print(f"\nassistant> {answer}")

        # Token usage per response
        pt= resp.usage.prompt_tokens
        ct= resp.usage.completion_tokens
        tt = resp.usage.total_tokens
        usage_totals["prompt"] += pt
        usage_totals["completion"] += ct
        usage_totals["total"] += tt
        
        print(f"[usage] prompt={pt} | completion={ct} | total={tt}")

    except Exception as e:
        print(f"[error] Chat request failed: {e}")
```

</details>

### 🌟 **Advanced Level Enhancements**

<details>
<summary>🔍 <strong>Click to see bonus features code</strong></summary>

```python
# Some lines to inspire you and complement your beginning challenge code

# Maybe you want to keep track of questions asked and total token usage? :-)
question_count = 0
usage_totals = {"prompt": 0, "completion": 0, "total": 0}

# And maybe your exit condition could also print a summary?
print(
    f"Goodbye {user_name}! You asked {question_count} question(s). "
    f"Total tokens used: {usage_totals['total']} "
    f"(prompt: {usage_totals['prompt']}, completion: {usage_totals['completion']})."
)

# Inside your try block, you might want to increment the question counter:
question_count += 1
```

</details>

---

## 🔧 **Key Changes from Original Example**

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0;">

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff;">

**🔄 From Static to Dynamic**
- Replace hardcoded question with `input()`
- Add `while True:` loop around chat completion

</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">

**👤 Personalization**
- Ask for user's name at startup
- Include name in system prompt

</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #dc3545;">

**🚪 Graceful Exit**
- Check for "quit" command
- Clean goodbye message

</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">

**📊 Continuous Tracking**
- Keep showing token usage
- Accumulate statistics

</div>

</div>

---

## ✅ **Success Criteria**

<div style="background: #d1ecf1; padding: 20px; border-radius: 10px; border-left: 4px solid #0c5460;">

**Your solution should achieve all of these:**

- ✅ User can have **multiple conversations** without restarting the program
- ✅ System **knows and uses** the user's name throughout
- ✅ User can **exit gracefully** by typing "quit"
- ✅ **Token usage** is still displayed after each response  
- ✅ Code is **clean and easy to understand**

</div>

---

## ⏱️ **Time Estimation**

<div align="center">

| Level | Time | What You'll Build |
|-------|------|-------------------|
| 🟢 **Basic** | 10-15 minutes | Interactive chat loop with personalization |
| 🟡 **Advanced** | +5 minutes | Enhanced with stats and summaries |

</div>

---

## 📦 **Deliverables**

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; margin: 15px 0;">

### 🎯 **What to Submit**

1. **📄 Modified Python file** → Save as `ex1-ch1-YOURNAME.py`
2. **🧪 Quick test** → Make sure it works end-to-end!

*Example: If your name is Maria, save as `ex1-ch1-maria.py`*

</div>

---

<div align="center">

## 🎉 **Ready to Build Your First Interactive AI Chat?**

*This is your first step toward building more sophisticated AI applications!*

**🚀 Let's turn that static example into a dynamic conversation! 🚀**

---

💡 **Pro Tip:** Start simple with the basic requirements, then add bonus features if you finish early!

</div>
