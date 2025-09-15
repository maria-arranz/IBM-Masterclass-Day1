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

# 1. Authentication / Client setup (AzureOpenAI)
# ---------------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint=azureServices_endpoint,
    api_version=azureServices_apiVersion,
    api_key=azureServices_key,
    azure_deployment=azureServices_deployment
)

# 2. Creating a Chat Completion Request using the client
# ---------------------------------------------------------------------

response = client.chat.completions.create(
    model=azureServices_deployment,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "We're in a great IBM Event in Barcelona. In my free time, what should I see?",
        }
    ]
)

# 3. Print the response with clear formatting and explanations
# ---------------------------------------------------------------------

# A) Print the actual assistant reply
print("\n" + "="*50)
print("🤖 Assistant Response")
print("="*50)
print(response.choices[0].message.content)
print("="*50 + "\n")

# B) Print token usage details in a clean format
print("📊 Token Usage Details")
print("-"*50)
print(f"Prompt tokens (input sent):      {response.usage.prompt_tokens}")
print(f"Completion tokens (AI response): {response.usage.completion_tokens}")
print(f"Total tokens (input + output):   {response.usage.total_tokens}")
print("-"*50 + "\n")