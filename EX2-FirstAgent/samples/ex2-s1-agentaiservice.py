import os
from azure.ai.projects import AIProjectClient
from azure.identity import ClientSecretCredential
from azure.ai.agents.models import ListSortOrder
from dotenv import load_dotenv


load_dotenv()

azure_foundry_project_endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")
azure_foundry_key = os.getenv("AI_FOUNDRY_API_KEY")
azure_foundry_deployment = os.getenv("AI_FOUNDRY_DEPLOYMENT_NAME")
varCredential = ClientSecretCredential(
    tenant_id=os.getenv("AZURE_TENANT_ID"),
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET"),
)

project = AIProjectClient(
    endpoint=azure_foundry_project_endpoint,
    credential=varCredential
)

agent = project.agents.create_agent(
    model=azure_foundry_deployment,
    name="IBM Super Cool Agent",
    instructions="You are a helpful assistant that helps users with their questions.",
)

thread = project.agents.threads.create()
message = project.agents.messages.create(
    thread_id=thread.id, 
    role="user", 
    content="Write me a poem about flowers")

run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
if run.status == "failed":
    # Check if you got "Rate limit is exceeded.", then you want to get more quota
    print(f"Run failed: {run.last_error}")

# Get messages from the thread
messages = project.agents.messages.list(thread_id=thread.id)

# Get the last message from the sender
messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
for message in messages:
    if message.run_id == run.id and message.text_messages:
        print(f"{message.role}: {message.text_messages[-1].text.value}")


