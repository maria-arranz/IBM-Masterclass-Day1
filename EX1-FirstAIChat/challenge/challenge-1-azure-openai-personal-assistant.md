# 🚀 Challenge 1: Interactive Chat Loop with Azure OpenAI

## Objective
Transform the single-question example into an interactive chat where users can have multiple conversations with the AI assistant.

## What You'll Learn
- Converting single-request code into interactive loops
- Basic user input handling
- Simple conversation flow management
- Practical application of the Azure OpenAI example

## Challenge Description
Based on the example `ex1-s1-aoai.py`, modify the code to create an interactive chat that:

1. **Asks the user their name** when starting
2. **Keeps asking for new questions** until the user types "quit"
3. **Uses the user's name** in the system prompt to personalize responses
4. **Shows token usage** after each response

## Technical Requirements

### Basic Level (10-15 minutes) ✅ MAIN GOAL
- [ ] Create a simple `while` loop for continuous conversation
- [ ] Ask for user's name at the beginning
- [ ] Include the user's name in the system prompt
- [ ] Allow user to type "quit" to exit
- [ ] Keep showing token usage after each response

### Advanced Level (Extra 5 minutes for fast finishers) 🌟 BONUS
- [ ] Keep track of how many questions the user has asked
- [ ] Add a goodbye message with conversation summary when quitting

## Getting Started Hints (Basic Level)
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
        print(
            f"Goodbye {user_name}!"
        )
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
## Getting Started Hints (Advanced Level)
```python
# Some lines to inspire you and complement your beginning challenge code

# Maybe you want to keep track of questions asked and total token usage? :-)
question_count = 0
usage_totals = {"prompt": 0, "completion": 0, "total": 0}

## And maybe your exit condition could also print a summary?
        f"Goodbye {user_name}! You asked {question_count} question(s). "
        f"Total tokens used: {usage_totals['total']} (prompt: {usage_totals['prompt']}, completion: {usage_totals['completion']})."

try:
        # your code in the beginning challenge + tracking question count 
        question_count += 1

```



## Key Changes from Original Example
1. **Replace the hardcoded question** with user input
2. **Add a loop** around the chat completion call
3. **Personalize the system prompt** with the user's name
4. **Add exit condition** when user types "quit"

## Success Criteria
- ✅ User can have multiple conversations without restarting the program
- ✅ System knows and uses the user's name
- ✅ User can exit gracefully
- ✅ Token usage is still displayed
- ✅ Code is clean and easy to understand

## Time Estimation
- **Basic Level**: 10-15 minutes
- **With Bonus Features**: 15-20 minutes

## Deliverables
1. Modified Python file (`ex1-ch1-YOURNAME.py`)
2. Quick test to make sure it works!

This is your first step toward building more sophisticated AI applications! 🚀
