"""
Interactive Chat Loop with Azure OpenAI (15‑min challenge)
----------------------------------------------------------
Basic + Bonus features:
- Asks for user's name
- While loop until user types 'quit'
- System prompt personalized with user's name
- Shows token usage after each response
- BONUS: /help command, question counter, summary on exit

Prereqs (env vars):
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_API_VERSION   (e.g. 2024-10-21)
- AZURE_OPENAI_DEPLOYMENT_NAME  (chat model deployment name)

All messages/logs in English.
"""
import os
import sys
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

client = AzureOpenAI(
    azure_endpoint=ENDPOINT,
    api_key=API_KEY,
    api_version=API_VERSION,
    azure_deployment=DEPLOYMENT,
)

print("🤖 Welcome to your AI Assistant! (type /help for options)")
user_name = input("What's your name? ").strip() or "friend"

question_count = 0
usage_totals = {"prompt": 0, "completion": 0, "total": 0}

HELP_TEXT = (
    "Available commands:\n"
    "  /help   Show this help\n"
    "  quit    Exit the chat\n"
)

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
            f"Goodbye {user_name}! You asked {question_count} question(s). "
            f"Total tokens used: {usage_totals['total']} (prompt: {usage_totals['prompt']}, completion: {usage_totals['completion']})."
        )
        break

    if user_input.lower() == "/help":
        print(HELP_TEXT)
        continue

    # Build a minimal message list (single-turn style) — simple for the 15-min challenge
    messages = [
        {"role": "system", "content": system_prompt(user_name)},
        {"role": "user", "content": user_input},
    ]

    try:
        resp = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=messages,
            temperature=0.7,
            max_completion_tokens=1000,
        )
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

        question_count += 1

    except Exception as e:
        print(f"[error] Chat request failed: {e}")
