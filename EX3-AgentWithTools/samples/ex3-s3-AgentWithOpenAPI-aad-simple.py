# Simple OpenAPI Tool Example for Azure AI Foundry Agents
# ---------------------------------------------------------------------
# This example demonstrates how to create an AI Agent with OpenAPI tool capabilities
# following Microsoft's official documentation pattern.
# 
# The agent can interact with an external Inventory Management API to:
#   - List inventory items
#   - Create new items
#   - Update stock levels
#   - Generate reports
# ---------------------------------------------------------------------

import os
import jsonref
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import OpenApiTool, OpenApiAnonymousAuthDetails
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get required environment variables
endpoint = os.environ["AI_FOUNDRY_ENDPOINT"]
model_deployment_name = os.environ["AI_FOUNDRY_DEPLOYMENT_NAME"]

def main():
    """
    Main function demonstrating OpenAPI agent capabilities.
    """
    print("🏭 Industrial Inventory Manager with OpenAPI Integration")
    print("=" * 70)
    
    # Initialize the project client using the endpoint and default credentials
    with AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
    ) as project_client:
        
        # Load the OpenAPI specification for the inventory service from a local JSON file
        print("📋 Loading OpenAPI specification...")
        try:
            with open(os.path.join(os.path.dirname(__file__), "openApiDef", "InventoryAPI.json"), "r") as f:
                openapi_inventory = jsonref.loads(f.read())
            print("✅ OpenAPI specification loaded successfully")
        except FileNotFoundError:
            print("❌ openApiDef/InventoryAPI.json not found. Please ensure it's in the openApiDef directory.")
            return
        except Exception as e:
            print(f"❌ Error loading OpenAPI spec: {e}")
            return
        
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
            - Searching and listing inventory items
            - Creating new inventory entries
            - Updating stock levels and item details
            - Managing item reservations
            - Generating low stock and utilization reports
            
            When users ask for inventory operations, use the available API functions to help them.
            Always provide clear, helpful responses about what you're doing and the results.""",
            tools=openapi_tool.definitions,
        )
        print(f"✅ Created agent, ID: {agent.id}")
        
        # Create a new conversation thread for the interaction
        thread = project_client.agents.threads.create()
        print(f"📝 Created thread, ID: {thread.id}")
        
        # Demo some basic operations first
        print("\n🎯 Running demo operations...")
        demo_requests = [
            "List all inventory items and show me a summary",
            "Generate a low stock report",
            "Show me all items in the 'components' category"
        ]
        
        for i, request in enumerate(demo_requests, 1):
            print(f"\n{i}. 📋 Demo request: {request}")
            
            # Create the user message
            message = project_client.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=request,
            )
            
            # Process the request
            print("   🔄 Processing...")
            run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
            
            if run.status == "completed":
                # Get the response
                messages = project_client.agents.messages.list(thread_id=thread.id)
                message_list = list(messages)
                for msg in reversed(message_list):
                    if msg.role == "assistant" and hasattr(msg, 'content'):
                        for content in msg.content:
                            if hasattr(content, 'text'):
                                response_text = content.text.value
                                # Truncate long responses for demo
                                if len(response_text) > 300:
                                    response_text = response_text[:300] + "...\n   [Response truncated for demo]"
                                print(f"   🤖 Response: {response_text}")
                        break
                
                # Show API calls made
                run_steps = project_client.agents.run_steps.list(thread_id=thread.id, run_id=run.id)
                for step in run_steps:
                    if hasattr(step.step_details, 'tool_calls'):
                        for call in step.step_details.tool_calls:
                            if hasattr(call, 'function'):
                                print(f"   🔧 API call: {call.function.name}")
                                
            elif run.status == "failed":
                print(f"   ❌ Request failed: {run.last_error}")
            else:
                print(f"   ⚠️ Request status: {run.status}")
        
        # Interactive session
        print("\n💬 Starting interactive inventory management session")
        print("Ask me about inventory operations, like:")
        print("• 'Create a new item for steel bolts with SKU BOLT-001'")
        print("• 'Update stock for item XYZ to 500 units'")
        print("• 'Reserve 50 units of ABC-123 for work order WO-001'")
        print("• 'Show utilization report for last 30 days'")
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
            
            # Create and automatically process the run
            print("🔄 Processing request...")
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
# 1. OpenAPI Tool Setup:
#    - Load spec with jsonref.loads() to resolve $ref links
#    - Use OpenApiAnonymousAuthDetails() for APIs without auth
#    - Create OpenApiTool with name, spec, description, and auth
#
# 2. Agent Creation:
#    - Use openapi_tool.definitions (not the tool object itself)
#    - Provide clear instructions about available operations
#
# 3. Request Processing:
#    - create_and_process() handles tool calls automatically
#    - Check run.status to ensure completion
#    - Extract responses from message history
#
# 4. Best Practices:
#    - Keep instructions clear and specific
#    - Handle errors gracefully
#    - Clean up resources when done
#    - Use context managers for client management
# ---------------------------------------------------------------------