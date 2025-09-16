"""
Industrial Inventory Manager with OpenAPI Integration - Service Principal Authentication
======================================================================================

This example demonstrates how to create an AI agent that integrates with external REST APIs 
using OpenAPI specifications with Service Principal authentication. The agent can perform 
complex inventory management operations by automatically calling REST endpoints based on 
natural language requests.

Following Microsoft's official documentation pattern for Azure AI Foundry Agent Service.

Key Features:
- OpenAPI 3.0 specification integration
- Automatic API endpoint discovery and calling
- Service Principal authentication for production scenarios
- Real-time inventory management operations
- Interactive conversation interface

Prerequisites:
- Azure AI Foundry project with deployed model
- Service Principal credentials configured
- InventoryAPI.json OpenAPI specification file
- Required Python packages (see requirements.txt)
"""

import os
import json
import jsonref
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import OpenApiTool, OpenApiAnonymousAuthDetails
from azure.identity import ClientSecretCredential

# Configuration from environment variables
endpoint = os.environ.get("AI_PROJECT_ENDPOINT")
model_deployment_name = os.environ.get("AI_MODEL_DEPLOYMENT_NAME", "gpt-4o")

# Service Principal credentials
tenant_id = os.environ.get("AZURE_TENANT_ID")
client_id = os.environ.get("AZURE_CLIENT_ID")
client_secret = os.environ.get("AZURE_CLIENT_SECRET")

def main():
    """
    Main function demonstrating OpenAPI agent capabilities with Service Principal authentication.
    """
    print("🏭 Industrial Inventory Manager with OpenAPI Integration (Service Principal)")
    print("=" * 80)
    
    # Create Service Principal credential
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Initialize the project client using the endpoint and Service Principal credentials
    with AIProjectClient(
        endpoint=endpoint,
        credential=credential,
    ) as project_client:
        
        # Load the OpenAPI specification for the inventory service from a local JSON file
        print("📋 Loading OpenAPI specification...")
        with open(os.path.join(os.path.dirname(__file__), "InventoryAPI.json"), "r") as f:
            openapi_inventory = jsonref.loads(f.read())
        
        # Create Auth object for the OpenApiTool (using anonymous auth since our demo API doesn't require authentication)
        auth = OpenApiAnonymousAuthDetails()
        
        # Initialize the main OpenAPI tool definition for inventory management
        print("🔧 Setting up OpenAPI tool...")
        openapi_tool = OpenApiTool(
            name="inventory_management", 
            spec=openapi_inventory, 
            description="Manage industrial inventory including materials, equipment, and consumables", 
            auth=auth
        )
        
        # Create an agent configured with the OpenAPI tool definitions
        print("🤖 Creating agent...")
        agent = project_client.agents.create_agent(
            model=model_deployment_name,
            name="Industrial Inventory Manager",
            instructions="""You are an Industrial Inventory Manager specialized in managing manufacturing inventory systems. 
            You help users with inventory operations like:
            - Searching for inventory items
            - Creating new inventory entries
            - Updating stock levels
            - Managing reservations
            - Generating reports
            
            Always provide clear, helpful responses about inventory operations.""",
            tools=openapi_tool.definitions,
        )
        print(f"✅ Created agent, ID: {agent.id}")
        
        # Create a new conversation thread for the interaction
        thread = project_client.agents.threads.create()
        print(f"📝 Created thread, ID: {thread.id}")
        
        # Interactive session
        print("\n💬 Starting interactive inventory management session")
        print("Ask me about inventory operations, like:")
        print("• 'List all inventory items'")
        print("• 'Show me items with low stock'")
        print("• 'Create a new inventory item for steel bolts'")
        print("• 'Generate a utilization report'")
        print("\nType 'quit' to exit")
        print("-" * 50)
        
        while True:
            user_input = input("\n📦 Your request: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                break
                
            if not user_input:
                continue
            
            # Create the user message in the thread
            message = project_client.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input,
            )
            
            # Create and automatically process the run, handling tool calls internally
            print("⚙️ Processing request...")
            run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
            
            if run.status == "completed":
                # Get and display the response
                messages = project_client.agents.messages.list(thread_id=thread.id)
                message_list = list(messages)
                for msg in reversed(message_list):
                    if msg.role == "assistant" and hasattr(msg, 'content'):
                        for content in msg.content:
                            if hasattr(content, 'text'):
                                print(f"\n🤖 Inventory Manager:\n{content.text.value}")
                        break
                        
            elif run.status == "failed":
                print(f"❌ Request failed: {run.last_error}")
            else:
                print(f"⚠️ Request status: {run.status}")
        
        # Cleanup
        print("\n🧹 Cleaning up...")
        project_client.agents.delete_agent(agent.id)
        print("✅ Agent deleted successfully")
        print("\n👋 Thank you for using the Industrial Inventory Manager!")

if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------
# Key Concepts:
# 
# 1. Service Principal Authentication:
#    - Use ClientSecretCredential for production scenarios
#    - Non-interactive authentication suitable for automation
#    - Requires AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET
#
# 2. OpenAPI Tool Setup:
#    - Load spec with jsonref.loads() to resolve $ref links
#    - Use OpenApiAnonymousAuthDetails() for APIs without auth
#    - Create OpenApiTool with name, spec, description, and auth
#
# 3. Agent Creation:
#    - Use openapi_tool.definitions (not the tool object itself)
#    - Provide clear instructions about available operations
#
# 4. Request Processing:
#    - create_and_process() handles tool calls automatically
#    - Check run.status to ensure completion
#    - Extract responses from message history
#
# 5. Best Practices:
#    - Keep instructions clear and specific
#    - Handle errors gracefully
#    - Clean up resources when done
#    - Use context managers for client management
# ---------------------------------------------------------------------