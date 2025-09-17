# 0. Import necessary libraries and set up environment variables
# ---------------------------------------------------------------------
import os
import jsonref
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder, OpenApiTool, OpenApiAnonymousAuthDetails
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# 1. Environment Variables Setup
# ---------------------------------------------------------------------
azure_foundry_project_endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")
azure_foundry_key = os.getenv("AI_FOUNDRY_API_KEY")
azure_foundry_deployment = os.getenv("AI_FOUNDRY_DEPLOYMENT_NAME")

# 2. Authentication Setup using DefaultAzureCredential
# ---------------------------------------------------------------------
# 3. AI Project Client Setup with context manager
# ---------------------------------------------------------------------

with AIProjectClient(
    endpoint=azure_foundry_project_endpoint,
    credential=DefaultAzureCredential()
) as project:

    # 4. Create the OpenAPI Tool loading the specification from a local file
    # ---------------------------------------------------------------------
    # Load the OpenAPI specification for the inventory service from a local JSON file
    with open(os.path.join(os.path.dirname(__file__), "./openApiDef/InventoryAPI.json"), "r") as f:
        openapi_inventory = jsonref.loads(f.read())

    # Create Auth object for the OpenApiTool (note: using anonymous auth here; connection or managed identity requires additional setup)
    auth = OpenApiAnonymousAuthDetails()

    # Initialize the main OpenAPI tool definition for inventory
    openapi_tool = OpenApiTool(
        name="get_inventory", 
        spec=openapi_inventory, 
        description="Retrieve inventory information for a location", 
        auth=auth
    )

    # 5. Agent Creation
    # ---------------------------------------------------------------------
    agent = project.agents.create_agent(
        model=azure_foundry_deployment,
        name="IBM Inventory Agent",
        instructions="You are a helpful assistant connected to an API that provides inventory information for IBM warehouses. Use the API to retrieve and manage inventory data as needed.",
        tools=openapi_tool.definitions,
    )

    # 6. Thread Creation
    # ---------------------------------------------------------------------
    thread = project.agents.threads.create()

    # 7. Message Creation
    # ---------------------------------------------------------------------
    message = project.agents.messages.create(
        thread_id=thread.id, 
        role="user", 
        content="Give me the full list of inventory items"
    )

    # 8. Run Creation and Processing
    # ---------------------------------------------------------------------
    run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

    # 9. Error Handling
    # ---------------------------------------------------------------------
    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")

    # 10. Retrieving and Displaying Messages
    # ---------------------------------------------------------------------
    messages = project.agents.messages.list(
        thread_id=thread.id, 
        order=ListSortOrder.ASCENDING
    )

    for message in messages:
        if message.run_id == run.id and message.text_messages:
            print(f"{message.role}: {message.text_messages[-1].text.value}")

