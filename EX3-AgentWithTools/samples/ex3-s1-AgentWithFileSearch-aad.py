# 0. Import necessary libraries and set up environment variables
# ---------------------------------------------------------------------
# This example demonstrates how to create an AI Agent with File Search capabilities
# using Azure AI Foundry. File Search allows agents to find and retrieve information
# from uploaded documents, making it perfect for:
#   - Technical documentation queries
#   - Policy and procedure lookups  
#   - Knowledge base interactions
#   - Industrial manual consultations
# ---------------------------------------------------------------------
import os
import time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import (
    FileSearchToolDefinition,
    ToolConnectionDefinition, 
    ConnectionType
)
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# 1. Environment Variables Setup
# ---------------------------------------------------------------------
# Required environment variables for Azure AI Foundry:
# - AI_FOUNDRY_ENDPOINT: Your Azure AI Foundry project endpoint
# - AI_FOUNDRY_DEPLOYMENT_NAME: The model deployment you want to use
#
# For File Search, the agent will automatically create and manage:
#   - Vector stores for document indexing
#   - File uploads and processing
#   - Search indexes for fast retrieval
# ---------------------------------------------------------------------
azure_foundry_project_endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")
azure_foundry_deployment = os.getenv("AI_FOUNDRY_DEPLOYMENT_NAME")

# 2. Authentication Setup using DefaultAzureCredential
# ---------------------------------------------------------------------
# DefaultAzureCredential automatically discovers and uses the best available credential:
#   1. Environment variables (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)
#   2. Managed Identity (for Azure-hosted applications)  
#   3. Visual Studio Code authentication
#   4. Azure CLI authentication (`az login`)
#   5. Interactive browser authentication (fallback)
#
# Perfect for development environments where you're already authenticated
# via Azure CLI or VS Code. No need to manage secrets locally.
# ---------------------------------------------------------------------

# 3. AI Project Client Setup
# ---------------------------------------------------------------------
project = AIProjectClient(
    endpoint=azure_foundry_project_endpoint,
    credential=DefaultAzureCredential()
)

# 4. File Search Tool Configuration
# ---------------------------------------------------------------------
# File Search is a powerful knowledge tool that enables agents to:
#   - Index uploaded documents automatically
#   - Perform semantic search across document content
#   - Extract relevant passages with citations
#   - Handle multiple document formats (PDF, TXT, DOCX, etc.)
#
# The tool creates vector embeddings of document content for fast,
# accurate search and retrieval during conversations.
# ---------------------------------------------------------------------

def create_industrial_knowledge_agent():
    """
    Creates an AI agent specialized in industrial documentation and knowledge lookup.
    
    Returns:
        tuple: (agent, vector_store) - The created agent and its vector store
    """
    print("🔧 Creating Industrial Knowledge Agent with File Search capabilities...")
    
    # Create a vector store for our industrial documents
    print("📁 Setting up document vector store...")
    vector_store = project.agents.create_vector_store(
        name="Industrial Knowledge Base",
        options={
            "expires_after": {
                "anchor": "last_active_at",
                "days": 7  # Auto-cleanup after 7 days of inactivity
            }
        }
    )
    
    # Create the File Search tool definition
    file_search_tool = FileSearchToolDefinition()
    
    # Create tool connection that links the tool to our vector store
    tool_connection = ToolConnectionDefinition(
        connection_type=ConnectionType.WORKSPACE_CONNECTION,
        connection_id=vector_store.id
    )
    
    # Create the agent with File Search capabilities
    print("🤖 Creating agent with File Search tool...")
    agent = project.agents.create_agent(
        model=azure_foundry_deployment,
        name="Industrial Knowledge Assistant",
        instructions="""You are an Industrial Knowledge Assistant specialized in helping with technical documentation, 
        maintenance procedures, safety protocols, and operational guidelines.

        Your expertise includes:
        - Equipment maintenance and troubleshooting procedures
        - Safety protocols and regulatory compliance
        - Operational best practices and standard procedures  
        - Technical specifications and equipment manuals
        - Quality control and inspection guidelines

        When using the File Search tool:
        1. Always search through the uploaded documents first before providing general knowledge
        2. Cite specific document sections, page numbers, or procedure steps when available
        3. If information isn't found in documents, clearly state this and offer to help with general knowledge
        4. Provide practical, actionable guidance based on the documentation
        5. Highlight any safety considerations or critical warnings found in the documents

        Be thorough, precise, and always prioritize safety in your recommendations.""",
        tools=[file_search_tool],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store.id]
            }
        }
    )
    
    print(f"✅ Agent created successfully!")
    print(f"   Agent ID: {agent.id}")
    print(f"   Vector Store ID: {vector_store.id}")
    
    return agent, vector_store

def upload_sample_documents(vector_store):
    """
    Upload sample industrial documents to demonstrate File Search capabilities.
    In a real scenario, users would upload their own technical manuals and documentation.
    
    Args:
        vector_store: The vector store to upload documents to
        
    Returns:
        list: List of uploaded file IDs
    """
    print("\n📄 Uploading sample industrial documentation...")
    
    # Sample content representing typical industrial documentation
    sample_docs = [
        {
            "filename": "equipment_maintenance_guide.txt",
            "content": """INDUSTRIAL EQUIPMENT MAINTENANCE GUIDE
============================================

SECTION 1: CONVEYOR BELT SYSTEM (Model CBX-3000)
-------------------------------------------------
Daily Inspection Checklist:
- Check belt tension (should deflect 2-3 inches under 10lb pressure)
- Inspect rollers for wear and proper rotation
- Lubricate bearing points with Grade 2 lithium grease
- Verify emergency stop functionality
- Check motor temperature (should not exceed 80°C)

Maintenance Schedule:
- Weekly: Clean debris from rollers and belt surface
- Monthly: Inspect and tighten all mounting bolts to 45 ft-lbs torque
- Quarterly: Replace drive belt if showing signs of cracking or fraying
- Annually: Full bearing replacement and electrical connection inspection

Troubleshooting:
Problem: Belt tracking off-center
Solution: Adjust tail pulley alignment using adjustment bolts
Torque: 25 ft-lbs

Problem: Excessive noise
Solution: Check for worn bearings or misaligned components
Action: Replace bearing assembly (Part #CBX-3000-BR-01)

SECTION 2: HYDRAULIC PRESS (Model HP-5000)
-------------------------------------------
Safety Requirements:
- ALWAYS engage safety locks before maintenance
- Maximum operating pressure: 3000 PSI
- Minimum operator distance: 3 feet during operation
- Required PPE: Safety glasses, steel-toed boots, hard hat

Monthly Maintenance:
1. Check hydraulic fluid level (maintain between MIN and MAX marks)
2. Inspect hoses for leaks or bulging (replace if cracked)
3. Test pressure relief valve at 3100 PSI
4. Lubricate pivot points with hydraulic oil ISO 46

Emergency Procedures:
- Red emergency stop button stops all hydraulic motion
- If hydraulic leak detected, immediately shut down and evacuate area
- Contact maintenance supervisor for all hydraulic repairs
"""
        },
        {
            "filename": "safety_protocols.txt", 
            "content": """INDUSTRIAL SAFETY PROTOCOLS AND PROCEDURES
==========================================

LOCKOUT/TAGOUT (LOTO) PROCEDURES
---------------------------------
Before performing maintenance on any powered equipment:

1. NOTIFY all affected personnel of impending shutdown
2. SHUTDOWN equipment using normal operating controls
3. ISOLATE energy sources:
   - Electrical: Open circuit breakers and remove fuses
   - Hydraulic: Close isolation valves and release pressure
   - Pneumatic: Close air supply valves and bleed lines
   - Steam: Close steam valves and allow cooling
4. LOCKOUT energy isolation devices with personal safety locks
5. TAGOUT with completed information tag including:
   - Worker name and date
   - Reason for lockout
   - Expected completion time
6. VERIFY energy isolation by attempting normal startup (should fail)

Personal Protective Equipment (PPE) Requirements:
-----------------------------------------------
Manufacturing Floor:
- Hard hat (ANSI Z89.1 Type I)
- Safety glasses with side shields
- Steel-toed boots (ASTM F2413)
- High-visibility vest in designated areas

Chemical Handling Areas:
- Chemical-resistant gloves (nitrile or neoprene)
- Chemical splash goggles
- Face shield for corrosive materials
- Chemical-resistant apron or suit

Welding Operations:
- Welding helmet with auto-darkening filter (Shade 9-13)
- Leather welding gloves and apron
- Fire-resistant clothing (no synthetic materials)
- Adequate ventilation or respiratory protection

Emergency Response Procedures:
-----------------------------
Fire Emergency:
1. Activate fire alarm immediately
2. Evacuate via nearest emergency exit
3. Proceed to designated assembly point
4. Report to area supervisor for headcount
5. Do NOT re-enter building until cleared by fire department

Chemical Spill:
1. Alert all personnel in immediate area
2. Evacuate spill area if hazardous
3. Contact emergency response team (Ext. 911)
4. Contain spill if safe to do so using spill kit materials
5. Provide Safety Data Sheet (SDS) to response team

Medical Emergency:
1. Do NOT move injured person unless in immediate danger
2. Call 911 and facility emergency number (Ext. 911)
3. Provide first aid only if trained and certified
4. Meet emergency responders at designated entrance
5. Complete incident report within 24 hours
"""
        }
    ]
    
    uploaded_files = []
    
    for doc in sample_docs:
        print(f"   Uploading: {doc['filename']}")
        
        # Create a temporary file
        temp_filename = f"/tmp/{doc['filename']}"
        with open(temp_filename, 'w', encoding='utf-8') as f:
            f.write(doc['content'])
        
        # Upload to vector store
        with open(temp_filename, 'rb') as file_stream:
            file_upload = project.agents.upload_file_and_add_to_vector_store(
                vector_store_id=vector_store.id,
                file_path=temp_filename,
                options={
                    "filename": doc['filename']
                }
            )
            uploaded_files.append(file_upload.id)
        
        # Clean up temp file
        os.remove(temp_filename)
    
    print(f"✅ Successfully uploaded {len(uploaded_files)} documents")
    return uploaded_files

def interactive_chat_with_documents(agent):
    """
    Start an interactive chat session with the industrial knowledge agent.
    
    Args:
        agent: The agent with File Search capabilities
    """
    print("\n🤖 Starting interactive chat with Industrial Knowledge Assistant")
    print("=" * 70)
    print("You can ask about:")
    print("• Equipment maintenance procedures")
    print("• Safety protocols and requirements") 
    print("• Troubleshooting guidance")
    print("• Operational best practices")
    print("\nType 'quit' to exit the conversation")
    print("=" * 70)
    
    # Create a conversation thread
    thread = project.agents.threads.create()
    
    while True:
        # Get user question
        user_question = input("\n❓ Your question: ").strip()
        
        if user_question.lower() in ['quit', 'exit', 'bye']:
            print("\n👋 Thank you for using the Industrial Knowledge Assistant!")
            break
        
        if not user_question:
            continue
        
        try:
            print("\n🔍 Searching through documentation...")
            
            # Create user message
            project.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_question
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
                        print(f"\n🤖 Assistant:")
                        for content in message.content:
                            if hasattr(content, 'text'):
                                print(content.text.value)
                            
                            # Show file citations if available
                            if hasattr(content, 'text') and hasattr(content.text, 'annotations'):
                                for annotation in content.text.annotations:
                                    if hasattr(annotation, 'file_citation'):
                                        print(f"\n📄 Source: {annotation.file_citation.filename}")
                        break
            else:
                print(f"❌ Run failed with status: {run.status}")
                
        except Exception as e:
            print(f"❌ Error processing question: {str(e)}")

def demonstrate_file_search_capabilities(agent, vector_store):
    """
    Demonstrate the File Search capabilities with predefined questions.
    
    Args:
        agent: The agent with File Search capabilities
        vector_store: The vector store containing documents
    """
    print("\n🎯 Demonstrating File Search Capabilities")
    print("=" * 50)
    
    # Predefined questions that showcase different aspects
    demo_questions = [
        "What is the proper torque specification for conveyor belt mounting bolts?",
        "What PPE is required for chemical handling operations?",
        "How do I troubleshoot a conveyor belt that's tracking off-center?",
        "What are the steps for LOCKOUT/TAGOUT procedures?",
        "What should I do if there's a hydraulic leak in the HP-5000 press?"
    ]
    
    # Create a conversation thread for the demo
    thread = project.agents.threads.create()
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n{i}. ❓ Question: {question}")
        print("   🔍 Searching documents...")
        
        try:
            # Create user message
            project.agents.messages.create(
                thread_id=thread.id,
                role="user", 
                content=question
            )
            
            # Run the agent
            run = project.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=agent.id
            )
            
            if run.status == "completed":
                # Get response
                messages = project.agents.messages.list(
                    thread_id=thread.id,
                    order="asc"
                )
                
                # Find latest assistant message
                for message in reversed(messages.data):
                    if message.role == "assistant" and message.run_id == run.id:
                        print(f"   🤖 Answer:")
                        for content in message.content:
                            if hasattr(content, 'text'):
                                # Truncate for demo purposes
                                text = content.text.value
                                if len(text) > 300:
                                    text = text[:300] + "..."
                                print(f"   {text}")
                                
                                # Show file citations
                                if hasattr(content.text, 'annotations'):
                                    for annotation in content.text.annotations:
                                        if hasattr(annotation, 'file_citation'):
                                            print(f"   📄 Source: {annotation.file_citation.filename}")
                        break
            else:
                print(f"   ❌ Failed: {run.status}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Brief pause between questions
        time.sleep(1)

# 5. Main Execution Flow
# ---------------------------------------------------------------------
def main():
    """
    Main function demonstrating File Search agent capabilities.
    """
    print("🏭 Industrial Knowledge Assistant with File Search")
    print("=" * 60)
    print("This example demonstrates how to create an AI agent that can:")
    print("• Search through uploaded technical documents")
    print("• Provide specific answers with document citations")
    print("• Handle industrial maintenance and safety queries")
    print("• Maintain conversation context across multiple questions")
    print("=" * 60)
    
    try:
        # Create the agent with File Search capabilities
        agent, vector_store = create_industrial_knowledge_agent()
        
        # Upload sample documents
        uploaded_files = upload_sample_documents(vector_store)
        
        # Wait for document processing
        print("\n⏳ Processing documents for search indexing...")
        time.sleep(3)  # Allow time for indexing
        
        # Demonstrate capabilities with predefined questions
        demonstrate_file_search_capabilities(agent, vector_store)
        
        # Start interactive chat
        interactive_chat_with_documents(agent)
        
    except Exception as e:
        print(f"❌ Error in main execution: {str(e)}")
        print("💡 Make sure your Azure AI Foundry credentials are properly configured")

if __name__ == "__main__":
    main()

# 6. Key Concepts and Best Practices
# ---------------------------------------------------------------------
# File Search Tool Benefits:
# • Automatic document indexing and vectorization
# • Semantic search across multiple document formats
# • Citation and source attribution for answers
# • Scalable to large document collections
# • No manual embedding management required
#
# Best Practices for File Search:
# • Use descriptive agent instructions to guide search behavior
# • Structure documents with clear headings and sections
# • Include metadata like document titles and categories
# • Test with various question types to verify search quality
# • Monitor vector store usage and implement cleanup policies
#
# Industrial Use Cases:
# • Technical manual consultation
# • Safety procedure verification
# • Troubleshooting guide searches
# • Regulatory compliance checks
# • Training material interactions
# • Quality control standard lookups
# ---------------------------------------------------------------------