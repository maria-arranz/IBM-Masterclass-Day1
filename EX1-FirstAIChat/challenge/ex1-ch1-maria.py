# 0. Import necessary libraries and set up environment variables
import os
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


print("🤖 Welcome to your AI Assistant!")
user_name = input("What's your name? ").strip()


def system_prompt(name: str) -> str:
    return (
        f"You are a helpful assistant. You are talking to {name}. "
        "Keep answers clear and concise."
    )

print(f"Hi {user_name}! Ask me anything. Type 'quit' to exit.")

usage_totals = {"prompt": 0, "completion": 0, "total": 0}
question_count = 0

while(True):
    user_input = input(f"\n{user_name}, what would you like to ask? ").strip()

    if user_input.lower() == "quit":
        print("\n[info] Exiting...")
        break

    messages = [
        {"role": "system", "content": system_prompt(user_name)},
        {"role": "user", "content": user_input},
    ]
    
    try:
        question_count += 1
        resp = client.chat.completions.create(
            model=azureServices_deployment,
            max_completion_tokens=1500,
            temperature=1.0,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            messages=messages)

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
    
print(
    f"Goodbye {user_name}! You asked {question_count} question(s). "
    f"Total tokens used: {usage_totals['total']} "
    f"(prompt: {usage_totals['prompt']}, completion: {usage_totals['completion']})."
)

