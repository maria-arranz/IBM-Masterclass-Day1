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
# To interact with Azure OpenAI you first need a client object.
# This client is responsible for:
#   - Knowing which Azure resource (endpoint) to talk to
#   - Handling authentication (API key or Azure Entra ID token)
#   - Optionally: setting default deployment, timeout, retries, etc.
#
# REQUIRED PARAMETERS:
# - azure_endpoint: Your Azure OpenAI resource endpoint.
# - api_version: API version string.
# - api_key: Indicates you want to use API key authentication.
# - azure_deployment: Default model deployment name.
#
# ADVANCED NETWORK / HTTP OPTIONS (optional):
# - timeout: Global timeout for requests (float or httpx.Timeout).
# - max_retries: How many times to retry transient errors (default is usually fine).
# - default_headers: Extra headers applied to every request.
# - default_query: Extra query params applied to every request.
# - http_client: A custom httpx.Client if you need proxy, connection pooling, etc.
#
# REALTIME / WEBHOOKS (rare in simple apps):
# - websocket_base_url: Base URL for WebSocket connections (Realtime API).
# - webhook_secret: Used to verify webhook signatures.
#
# OTHER:
# - _strict_response_validation: Validate API responses against schema (useful in debug).
# ---------------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint=azureServices_endpoint,
    api_version=azureServices_apiVersion,
    api_key=azureServices_key,
    azure_deployment=azureServices_deployment
)

# 2. Creating a Chat Completion Request using the client
# When you send a request to Azure OpenAI, you need to provide some information so the service knows 
# which model to use and how to answer. The key parts are:
#
# Required parameters:
# - model: The specific model you want to use. This is configured in your Azure OpenAI resource.
# - Messages: The conversation you send, broken down by roles: 
#   * system: overall instructions (e.g., "You are an educational assistant").
#   * user: what the person writes or asks.
#   * assistant: what the AI responds.
#
# Additional optional parameters:
## - stream: Boolean, default false. whether to send back the response in chunks (useful for real-time applications). 
## - max_completion_tokens: The maximum length of the answer, measured in "tokens" (small chunks of text).
## - Temperature: Controls how creative vs. predictable the answer is.
#   * Low = safer, more repetitive answers.
#   * High = more creative, varied answers.
## - top_p: Another way to control diversity. Instead of randomness, it tells the model 
#   to only pick from the most likely options.
## - frequency_penalty: Reduces how much the AI repeats the same words.
## - presence_penalty: Encourages the AI to bring in new ideas instead of sticking 
#   to what's already said.

response = client.chat.completions.create(
    model=azureServices_deployment,
    max_completion_tokens=1500,
    temperature=1.0,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
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
# At this stage we want to display two things:
#   A) The content of the AI's reply (what the assistant actually said).
#   B) A breakdown of how many tokens were used.
#      - Prompt tokens: what we sent in (system + user messages).
#      - Completion tokens: what the model generated in its response.
#      - Total tokens: sum of both, useful for cost calculation.
# This helps users not only see the output, but also understand the cost/usage impact.
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