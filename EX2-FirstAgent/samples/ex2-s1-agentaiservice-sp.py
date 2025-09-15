# 0. Import necessary libraries and set up environment variables
# ---------------------------------------------------------------------
# This example demonstrates how to create and use an AI Agent using Azure AI Foundry.
# Unlike direct chat completions, agents provide a higher-level abstraction that can:
#   - Maintain conversation context automatically
#   - Execute tools and functions
#   - Handle complex multi-turn conversations
#   - Manage their own internal state and memory
# ---------------------------------------------------------------------
import os
from azure.ai.projects import AIProjectClient
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# 1. Environment Variables Setup
# ---------------------------------------------------------------------
# Azure AI Foundry requires different authentication than basic Azure OpenAI:
# - AI_FOUNDRY_ENDPOINT: Your Azure AI Foundry project endpoint
# - AI_FOUNDRY_API_KEY: API key for your AI Foundry project
# - AI_FOUNDRY_DEPLOYMENT_NAME: The model deployment you want to use
# - AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET: Azure AD credentials
#
# AI Foundry provides a managed environment for AI applications with:
#   - Built-in agent orchestration
#   - Automatic conversation management
#   - Tool integration capabilities
#   - Enhanced security and compliance features
# ---------------------------------------------------------------------
azure_foundry_project_endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")
azure_foundry_key = os.getenv("AI_FOUNDRY_API_KEY")
azure_foundry_deployment = os.getenv("AI_FOUNDRY_DEPLOYMENT_NAME")

# 2. Authentication Setup using Azure Service Principal
# ---------------------------------------------------------------------
# Azure AI Foundry uses Azure Active Directory (Entra ID) for authentication.
# ClientSecretCredential is used for service-to-service authentication:
#
# REQUIRED CREDENTIALS:
# - tenant_id: Your Azure AD tenant identifier
# - client_id: Application (client) ID of your registered app
# - client_secret: Secret value of your registered app
#
# This authentication method is more secure than API keys and provides:
#   - Fine-grained access control through Azure RBAC
#   - Audit trails for security compliance
#   - Token-based authentication with automatic renewal
#   - Integration with Azure security policies
# ---------------------------------------------------------------------
varCredential = ClientSecretCredential(
    tenant_id=os.getenv("AZURE_TENANT_ID"),
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET"),
)

# 3. AI Project Client Setup
# ---------------------------------------------------------------------
# AIProjectClient is the main interface to interact with Azure AI Foundry.
# This client provides access to:
#   - Agent creation and management
#   - Thread (conversation) management
#   - Message handling within threads
#   - Run execution and monitoring
#
# The client handles:
#   - Connection pooling and retries
#   - Authentication token management
#   - Request/response serialization
#   - Error handling and status reporting
# ---------------------------------------------------------------------
project = AIProjectClient(
    endpoint=azure_foundry_project_endpoint,
    credential=varCredential
)

# 4. Agent Creation
# ---------------------------------------------------------------------
# An agent in Azure AI Foundry is a persistent AI entity that can:
#   - Maintain its own personality and instructions
#   - Remember context across conversations
#   - Execute tools and functions when needed
#   - Handle complex multi-step tasks
#
# AGENT PARAMETERS:
# - model: The underlying language model deployment to use
# - name: Human-readable name for identification and debugging
# - instructions: System prompt that defines the agent's behavior and personality
#
# OPTIONAL PARAMETERS (not used here but available):
# - tools: List of tools/functions the agent can execute
# - file_ids: Files the agent can access for knowledge
# - metadata: Custom key-value pairs for tracking
# - temperature: Controls response creativity (0.0-2.0)
# - top_p: Controls response diversity (0.0-1.0)
# ---------------------------------------------------------------------
agent = project.agents.create_agent(
    model=azure_foundry_deployment,
    name="IBM Super Cool Agent",
    instructions="You are a helpful assistant that helps users with their questions.",
)

# 5. Thread Creation
# ---------------------------------------------------------------------
# A thread represents a conversation session between a user and an agent.
# Think of it as a chat room where:
#   - All messages are stored in chronological order
#   - Context is maintained throughout the conversation
#   - Multiple users can participate (in advanced scenarios)
#   - The agent remembers previous messages automatically
#
# Threads provide:
#   - Conversation persistence across multiple interactions
#   - Automatic context management (no need to send full history)
#   - Message ordering and threading
#   - Metadata and tagging capabilities
# ---------------------------------------------------------------------
thread = project.agents.threads.create()

# 6. Message Creation
# ---------------------------------------------------------------------
# Messages are the individual communications within a thread.
# Each message has:
#   - thread_id: Associates the message with a specific conversation
#   - role: Either "user" (human input) or "assistant" (AI response)
#   - content: The actual text content of the message
#
# MESSAGE TYPES SUPPORTED:
# - Text messages: Plain text communication
# - File attachments: Documents, images, etc. (not used here)
# - System messages: Internal instructions (handled automatically)
#
# The agent will automatically see all previous messages in the thread
# when processing new messages, maintaining full conversational context.
# ---------------------------------------------------------------------
message = project.agents.messages.create(
    thread_id=thread.id, 
    role="user", 
    content="Write me a poem about flowers")

# 7. Run Creation and Processing
# ---------------------------------------------------------------------
# A "run" represents the agent's execution of a task within a thread.
# When you create a run, the agent:
#   1. Analyzes all messages in the thread for context
#   2. Processes the latest user message
#   3. Generates an appropriate response
#   4. Executes any required tools/functions (if configured)
#   5. Updates the thread with the response
#
# create_and_process() is a convenience method that:
#   - Creates the run
#   - Waits for completion
#   - Handles any required tool executions automatically
#   - Returns the final status
#
# RUN STATUSES:
# - "queued": Waiting to be processed
# - "in_progress": Currently being executed
# - "completed": Successfully finished
# - "failed": Encountered an error
# - "requires_action": Waiting for tool confirmation (advanced scenarios)
# ---------------------------------------------------------------------
run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

# 8. Error Handling
# ---------------------------------------------------------------------
# Always check the run status to ensure successful completion.
# Common failure reasons include:
#   - Rate limiting: Too many requests in a short time
#   - Model errors: Issues with the underlying language model
#   - Authentication problems: Invalid or expired credentials
#   - Network issues: Connectivity problems
#   - Resource limits: Quota exceeded or insufficient resources
#
# If you encounter rate limiting, you may need to:
#   - Request higher quota limits from Azure
#   - Implement retry logic with exponential backoff
#   - Optimize your request frequency
# ---------------------------------------------------------------------
if run.status == "failed":
    # Check if you got "Rate limit is exceeded.", then you want to get more quota
    print(f"Run failed: {run.last_error}")

# 9. Retrieving and Displaying Messages
# ---------------------------------------------------------------------
# After a successful run, the agent's response will be added to the thread.
# We need to retrieve messages to see the conversation history.
# ---------------------------------------------------------------------

# Get messages from the thread
messages = project.agents.messages.list(thread_id=thread.id)

# 10. Process and Display Agent Response
# ---------------------------------------------------------------------
# The agent's response will be in the thread as a new message.
# We filter for messages that:
#   - Were created during our specific run (message.run_id == run.id)
#   - Have text content (message.text_messages exists)
#
# MESSAGE STRUCTURE:
# - role: "assistant" for agent responses, "user" for human messages
# - text_messages: Array of text content blocks
# - text.value: The actual text content of the message
#
# MESSAGE RETRIEVAL OPTIONS:
# - List all messages: Gets complete conversation history
# - Filter by run_id: Gets only messages from a specific run
# - Order control: ASCENDING (oldest first) or DESCENDING (newest first)
# - Pagination: Handle large conversations efficiently

#
# Note: text_messages[-1] gets the last text block, which contains
# the final response from the agent.
# ---------------------------------------------------------------------

# Get the last message from the sender
messages = project.agents.messages.list(
    thread_id=thread.id, 
    order=ListSortOrder.ASCENDING
    )

for message in messages:
    if message.run_id == run.id and message.text_messages:
        print(f"{message.role}: {message.text_messages[-1].text.value}")

# 11. Summary of What Happened
# ---------------------------------------------------------------------
# This example demonstrated the complete AI Agent workflow:
#
# 1. SETUP: Configured authentication and project connection
# 2. AGENT: Created a persistent AI agent with specific instructions
# 3. THREAD: Started a new conversation session
# 4. MESSAGE: Added a user message to the conversation
# 5. RUN: Executed the agent to process and respond
# 6. RESULT: Retrieved and displayed the agent's response
#
# KEY ADVANTAGES OF AGENTS vs DIRECT CHAT COMPLETIONS:
# - Automatic context management (no need to manage conversation history)
# - Persistent agent personality and capabilities
# - Built-in error handling and retry logic
# - Tool integration capabilities for complex tasks
# - Scalable conversation management
# - Enhanced monitoring and debugging features
#
# NEXT STEPS:
# - Try different instructions to change agent behavior
# - Add more messages to see conversation context in action
# - Explore tool integration for function calling
# - Implement error handling and retry logic for production use
# ---------------------------------------------------------------------


