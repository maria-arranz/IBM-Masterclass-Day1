# 0. Import necessary libraries and set up environment variables
# ---------------------------------------------------------------------
# This example demonstrates how to create an AI Agent with OpenAPI tool capabilities
# using Azure AI Foundry. OpenAPI tools allow agents to:
#   - Integrate with external REST APIs and services
#   - Perform CRUD operations on external systems
#   - Access real-time data from enterprise applications
#   - Automate business processes across multiple systems
#   - Provide unified interface to complex API ecosystems
# ---------------------------------------------------------------------
import os
import json
from azure.ai.projects import AIProjectClient
from azure.identity import ClientSecretCredential
from azure.ai.projects.models import OpenAPIToolDefinition
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# 1. Environment Variables Setup
# ---------------------------------------------------------------------
# Required environment variables for Azure AI Foundry with Service Principal:
# - AI_FOUNDRY_ENDPOINT: Your Azure AI Foundry project endpoint
# - AI_FOUNDRY_DEPLOYMENT_NAME: The model deployment you want to use
# - AZURE_TENANT_ID: Your Azure Active Directory tenant ID
# - AZURE_CLIENT_ID: Your service principal application ID
# - AZURE_CLIENT_SECRET: Your service principal secret
#
# OpenAPI tools provide:
#   - Integration with REST APIs using OpenAPI specifications
#   - Automatic request/response handling and validation
#   - Support for authentication (API keys, OAuth, etc.)
#   - Schema-driven parameter validation
#   - Real-time data access from external systems
# ---------------------------------------------------------------------
azure_foundry_project_endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")
azure_foundry_deployment = os.getenv("AI_FOUNDRY_DEPLOYMENT_NAME")
azure_tenant_id = os.getenv("AZURE_TENANT_ID")
azure_client_id = os.getenv("AZURE_CLIENT_ID")
azure_client_secret = os.getenv("AZURE_CLIENT_SECRET")

# 2. Authentication Setup using Service Principal (ClientSecretCredential)
# ---------------------------------------------------------------------
# Service Principal authentication provides:
#   - Non-interactive authentication for production scenarios
#   - Fine-grained access control with Azure RBAC
#   - Ability to run in automated/headless environments
#   - Secure credential management for CI/CD pipelines
#
# To create a Service Principal:
#   1. Register an application in Azure AD
#   2. Create a client secret for the application  
#   3. Assign appropriate roles to the service principal
#   4. Configure the required environment variables
#
# This method is ideal for:
#   - Production deployments
#   - Automated systems and scripts
#   - CI/CD pipelines
#   - Multi-tenant applications
# ---------------------------------------------------------------------

# 3. AI Project Client Setup
# ---------------------------------------------------------------------
credential = ClientSecretCredential(
    tenant_id=azure_tenant_id,
    client_id=azure_client_id,
    client_secret=azure_client_secret
)

project = AIProjectClient(
    endpoint=azure_foundry_project_endpoint,
    credential=credential
)

# 4. OpenAPI Tool Configuration
# ---------------------------------------------------------------------
# OpenAPI tools enable agents to interact with external APIs by:
#   - Loading and parsing OpenAPI specifications
#   - Automatically generating function calls from API endpoints
#   - Handling authentication headers and parameters
#   - Validating requests and responses against schemas
#   - Providing error handling and retry logic
#
# Benefits:
#   - No manual API client code needed
#   - Schema validation ensures data integrity
#   - Automatic documentation from OpenAPI spec
#   - Standardized REST API integration pattern
# ---------------------------------------------------------------------

def load_openapi_specification():
    """
    Load the OpenAPI specification for the Industrial Inventory Management API.
    
    Returns:
        dict: The parsed OpenAPI specification
    """
    spec_path = os.path.join(os.path.dirname(__file__), "InventoryAPI.json")
    
    try:
        with open(os.path.join(os.path.dirname(__file__), "openApiDef", "InventoryAPI.json"), "r") as f:
            spec = json.load(f)
        print(f"✅ Loaded OpenAPI specification from {spec_path}")
        return spec
    except FileNotFoundError:
        print(f"❌ OpenAPI specification file not found: {spec_path}")
        print("💡 Make sure InventoryAPI.json is in the same directory as this script")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing OpenAPI specification: {e}")
        return None

def create_inventory_management_agent():
    """
    Creates an AI agent specialized in inventory management with OpenAPI tools.
    
    Returns:
        agent: The created agent with OpenAPI capabilities
    """
    print("📦 Creating Inventory Management Agent with OpenAPI tools...")
    
    # Load OpenAPI specification
    openapi_spec = load_openapi_specification()
    if not openapi_spec:
        return None
    
    # Create OpenAPI tool definition
    print("🔧 Configuring OpenAPI tool with Inventory Management API...")
    openapi_tool = OpenAPIToolDefinition(
        name="inventory_management_api",
        spec=openapi_spec
    )
    
    # Create the agent with OpenAPI capabilities
    print("🤖 Creating agent with OpenAPI tool...")
    agent = project.agents.create_agent(
        model=azure_foundry_deployment,
        name="Industrial Inventory Manager",
        instructions="""You are an Industrial Inventory Manager specialized in managing manufacturing inventory systems. 
        You have access to a comprehensive Inventory Management API that allows you to:

        **Core Capabilities:**
        - View and search inventory items across all categories
        - Create new inventory items with proper categorization
        - Update item details, stock levels, and locations
        - Delete items when they're no longer needed
        - Reserve items for production orders and maintenance
        - Generate reports on stock levels and utilization

        **Inventory Categories:**
        - Raw Materials: Base materials for production
        - Components: Parts and sub-assemblies  
        - Tools: Manufacturing and maintenance tools
        - Equipment: Machinery and heavy equipment
        - Consumables: Supplies that are used up (oils, filters, etc.)
        - Finished Goods: Completed products ready for shipment

        **Key Operations:**
        1. **Inventory Search & Reporting:**
           - Use listInventoryItems to search and filter items
           - Generate low stock reports with getLowStockReport
           - Create utilization reports with getUtilizationReport
           - Filter by category, location, status, or stock levels

        2. **Item Management:**
           - Create new items with createInventoryItem
           - Update existing items with updateInventoryItem
           - View detailed item information with getInventoryItem
           - Delete obsolete items with deleteInventoryItem

        3. **Stock Operations:**
           - Adjust stock levels with updateItemStock
           - Reserve items for work orders with reserveInventoryItem
           - Track all stock movements with transaction history

        4. **Location Management:**
           - View all storage locations with listLocations
           - Organize items by warehouse, bins, shelves, and racks

        **Best Practices:**
        - Always validate item availability before making reservations
        - Provide clear reasons for stock adjustments
        - Use appropriate categories for new items
        - Monitor minimum stock levels to prevent shortages
        - Include reference numbers for traceability

        **Error Handling:**
        - If an API call fails, explain the error and suggest alternatives
        - Check for sufficient stock before reservations
        - Validate required fields before creating items
        - Handle authentication and permission errors gracefully

        **Response Format:**
        - Provide clear, structured responses about inventory operations
        - Include relevant item details (SKU, current stock, location)
        - Summarize the results of bulk operations
        - Suggest next steps when appropriate
        - Use tables for multi-item reports when helpful

        Always prioritize data accuracy and provide actionable insights for industrial operations.""",
        tools=[openapi_tool]
    )
    
    print(f"✅ Agent created successfully!")
    print(f"   Agent ID: {agent.id}")
    print(f"   Available API Operations: {len(openapi_spec.get('paths', {}))}")
    
    return agent

def demonstrate_inventory_operations(agent):
    """
    Demonstrate various inventory management operations.
    
    Args:
        agent: The agent with OpenAPI capabilities
    """
    print("\n🎯 Demonstrating Inventory Management Operations")
    print("=" * 60)
    
    # Create a conversation thread for demonstrations
    thread = project.agents.threads.create()
    
    # Predefined inventory management tasks
    demo_tasks = [
        {
            "task": "List all inventory items and show me a summary by category",
            "description": "Basic inventory overview with categorization"
        },
        {
            "task": "Generate a low stock report to identify items that need reordering",
            "description": "Stock level monitoring and alerts"
        },
        {
            "task": "Search for all items in the 'components' category that are currently available",
            "description": "Filtered inventory search by category and status"
        },
        {
            "task": "Show me the utilization report for the last 30 days to analyze inventory turnover",
            "description": "Performance analytics and reporting"
        },
        {
            "task": "Create a new inventory item: SKU 'BOLT-M12-100', name 'M12x100 Hex Bolt', category 'components', minimum stock 500 pieces, location 'BIN-A-15'",
            "description": "Creating new inventory items with proper categorization"
        }
    ]
    
    for i, demo in enumerate(demo_tasks, 1):
        print(f"\n{i}. 📋 Task: {demo['task']}")
        print(f"   📝 Purpose: {demo['description']}")
        print("   🔄 Processing request...")
        
        try:
            # Create user message with the task
            project.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=demo['task']
            )
            
            # Run the agent
            run = project.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=agent.id
            )
            
            if run.status == "completed":
                # Get the response
                messages = project.agents.messages.list(
                    thread_id=thread.id,
                    order="asc"
                )
                
                # Find the latest assistant message
                for message in reversed(messages.data):
                    if message.role == "assistant" and message.run_id == run.id:
                        print(f"   🤖 Inventory Manager Response:")
                        for content in message.content:
                            if hasattr(content, 'text'):
                                # Show truncated response for demo
                                text = content.text.value
                                if len(text) > 800:
                                    text = text[:800] + "...\n   [Response truncated for demo]"
                                print(f"   {text}")
                        break
            else:
                print(f"   ❌ Task failed with status: {run.status}")
                if hasattr(run, 'last_error') and run.last_error:
                    print(f"   Error: {run.last_error}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Brief pause between demonstrations
        import time
        time.sleep(2)

def interactive_inventory_management(agent):
    """
    Start an interactive inventory management session with the agent.
    
    Args:
        agent: The agent with OpenAPI capabilities
    """
    print("\n📦 Starting Interactive Inventory Management Session")
    print("=" * 70)
    print("You can ask the Inventory Manager to:")
    print("• Search and filter inventory items")
    print("• Create, update, or delete inventory items")
    print("• Adjust stock levels and manage reservations")
    print("• Generate reports and analytics")
    print("• Manage storage locations and organization")
    print("\nExample requests:")
    print("• 'Show me all tools with stock below minimum levels'")
    print("• 'Create a new raw material entry for steel sheets'")
    print("• 'Reserve 50 units of SKU ABC-123 for work order WO-2024-001'")
    print("• 'Update the location of item XYZ-789 to warehouse section B'")
    print("• 'Generate a utilization report for consumables this month'")
    print("\nType 'quit' to exit the session")
    print("=" * 70)
    
    # Create a conversation thread
    thread = project.agents.threads.create()
    
    while True:
        # Get user request
        user_request = input("\n📋 Your inventory request: ").strip()
        
        if user_request.lower() in ['quit', 'exit', 'bye']:
            print("\n👋 Thank you for using the Industrial Inventory Manager!")
            break
        
        if not user_request:
            continue
        
        try:
            print("\n🔄 Processing your inventory request...")
            
            # Create user message
            project.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_request
            )
            
            # Run the agent
            run = project.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=agent.id
            )
            
            if run.status == "completed":
                # Get the assistant's response
                messages = project.agents.messages.list(
                    thread_id=thread.id,
                    order="asc"
                )
                
                # Find the latest assistant message
                for message in reversed(messages.data):
                    if message.role == "assistant" and message.run_id == run.id:
                        print(f"\n🤖 Inventory Manager:")
                        for content in message.content:
                            if hasattr(content, 'text'):
                                print(content.text.value)
                        break
            else:
                print(f"❌ Request failed with status: {run.status}")
                if hasattr(run, 'last_error') and run.last_error:
                    print(f"Error details: {run.last_error}")
                
        except Exception as e:
            print(f"❌ Error processing request: {str(e)}")

def show_api_capabilities():
    """
    Display the capabilities of the Inventory Management API.
    """
    print("\n📋 Inventory Management API Capabilities")
    print("=" * 50)
    
    capabilities = {
        "📦 Item Management": [
            "List and search inventory items with filtering",
            "Create new inventory items with validation",
            "Update existing item properties and details",
            "Delete items (with reservation checks)",
            "View detailed item information and history"
        ],
        "📊 Stock Operations": [
            "Adjust stock levels (add, remove, set)",
            "Reserve items for production orders",
            "Track stock movements and transactions",
            "Monitor stock thresholds and alerts",
            "Handle different units of measurement"
        ],
        "📍 Location Management": [
            "Manage warehouse locations and bins",
            "Organize items by storage areas",
            "Track location utilization",
            "Support hierarchical location structures"
        ],
        "📈 Reporting & Analytics": [
            "Generate low stock alerts and reports",
            "Create utilization and turnover reports",
            "Analyze inventory performance trends",
            "Track category-wise metrics",
            "Export data for external analysis"
        ],
        "🔒 Security & Audit": [
            "API key authentication",
            "Transaction logging and history",
            "User tracking for all operations",
            "Reference number validation",
            "Error handling and validation"
        ]
    }
    
    for category, features in capabilities.items():
        print(f"\n{category}:")
        for feature in features:
            print(f"   • {feature}")
    
    print(f"\n✅ Total API Endpoints: 12")
    print(f"📁 Categories Supported: 6 (Raw Materials, Components, Tools, Equipment, Consumables, Finished Goods)")
    print(f"🔄 Operations: CRUD + Search + Reports + Reservations")

# 5. Main Execution Flow
# ---------------------------------------------------------------------
def main():
    """
    Main function demonstrating OpenAPI agent capabilities.
    """
    print("🏭 Industrial Inventory Manager with OpenAPI Integration")
    print("=" * 70)
    print("This example demonstrates how to create an AI agent that can:")
    print("• Integrate with external REST APIs using OpenAPI specifications")
    print("• Perform complex inventory management operations")
    print("• Handle real-time data access and updates")
    print("• Provide unified interface to enterprise systems")
    print("• Automate business processes across API ecosystems")
    print("=" * 70)
    
    try:
        # Show API capabilities first
        show_api_capabilities()
        
        # Create the agent with OpenAPI capabilities
        agent = create_inventory_management_agent()
        if not agent:
            print("❌ Failed to create agent. Please check the OpenAPI specification file.")
            return
        
        # Demonstrate various inventory operations
        demonstrate_inventory_operations(agent)
        
        # Start interactive management session
        interactive_inventory_management(agent)
        
    except Exception as e:
        print(f"❌ Error in main execution: {str(e)}")
        print("💡 Make sure your Azure AI Foundry credentials are properly configured")
        print("💡 Ensure the InventoryAPI.json file is in the same directory")

if __name__ == "__main__":
    main()

# 6. Key Concepts and Best Practices
# ---------------------------------------------------------------------
# OpenAPI Tool Benefits:
# • Schema-driven API integration with automatic validation
# • No manual API client code required
# • Standardized REST API interaction patterns
# • Built-in authentication and error handling
# • Self-documenting through OpenAPI specifications
# • Support for complex request/response structures
#
# Best Practices for OpenAPI Tools:
# • Provide comprehensive OpenAPI specifications with examples
# • Include proper authentication mechanisms
# • Use descriptive operation IDs and parameter names
# • Implement proper error responses and status codes
# • Add detailed descriptions for all endpoints and schemas
# • Test API specifications thoroughly before integration
#
# Industrial Use Cases:
# • ERP system integration for inventory management
# • MES (Manufacturing Execution System) connectivity
# • Quality management system data access
# • Supplier portal integration
# • Asset management system integration
# • Production planning system connectivity
# • Maintenance management system integration
# ---------------------------------------------------------------------