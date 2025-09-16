# 0. Import necessary libraries and set up environment variables
# ---------------------------------------------------------------------
# This example demonstrates how to create an AI Agent with Code Interpreter capabilities
# using Azure AI Foundry. Code Interpreter allows agents to:
#   - Write and execute Python code in a secure sandbox
#   - Perform data analysis and visualization
#   - Handle complex mathematical calculations
#   - Generate charts, graphs, and reports
#   - Process files and create downloadable outputs
# ---------------------------------------------------------------------
import os
import time
from azure.ai.projects import AIProjectClient
from azure.identity import ClientSecretCredential
from azure.ai.projects.models import CodeInterpreterToolDefinition
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
# Code Interpreter provides:
#   - Secure Python execution environment (sandbox)
#   - Access to popular data science libraries (pandas, matplotlib, numpy, etc.)
#   - File upload and download capabilities
#   - Session persistence during conversations
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

# 4. Code Interpreter Tool Configuration
# ---------------------------------------------------------------------
# Code Interpreter is a powerful action tool that enables agents to:
#   - Execute Python code in a secure, isolated environment
#   - Access pre-installed libraries: pandas, numpy, matplotlib, seaborn, scipy, etc.
#   - Upload and process data files (CSV, JSON, Excel, etc.)
#   - Generate visualizations and downloadable files
#   - Perform statistical analysis and machine learning tasks
#
# Security features:
#   - Sandboxed execution environment
#   - No internet access from code
#   - Automatic session cleanup
#   - File access restrictions
# ---------------------------------------------------------------------

def create_data_analysis_agent():
    """
    Creates an AI agent specialized in data analysis and code execution.
    
    Returns:
        agent: The created agent with Code Interpreter capabilities
    """
    print("📊 Creating Data Analysis Agent with Code Interpreter capabilities...")
    
    # Create the Code Interpreter tool definition
    code_interpreter_tool = CodeInterpreterToolDefinition()
    
    # Create the agent with Code Interpreter capabilities
    print("🤖 Creating agent with Code Interpreter tool...")
    agent = project.agents.create_agent(
        model=azure_foundry_deployment,
        name="Industrial Data Analyst",
        instructions="""You are an Industrial Data Analyst specialized in manufacturing and operational data analysis. 
        You excel at processing industrial data, creating visualizations, and providing actionable insights.

        Your expertise includes:
        - Manufacturing KPI analysis (OEE, throughput, quality metrics)
        - Equipment performance monitoring and trends
        - Production scheduling optimization
        - Quality control statistical analysis
        - Energy consumption and efficiency analysis
        - Predictive maintenance data analysis

        When using the Code Interpreter:
        1. Always explain what you're going to do before writing code
        2. Write clean, well-commented Python code
        3. Use appropriate libraries (pandas for data, matplotlib/seaborn for visualization)
        4. Validate data quality and handle missing values appropriately
        5. Create clear, professional visualizations with proper titles and labels
        6. Provide statistical summaries and actionable insights
        7. Suggest next steps or recommendations based on the analysis

        Code style guidelines:
        - Use descriptive variable names
        - Add comments explaining complex logic
        - Include error handling for data operations
        - Format numbers appropriately for industrial contexts
        - Use industry-standard charts and metrics

        Always provide both the code and a clear explanation of the results and their implications for industrial operations.""",
        tools=[code_interpreter_tool]
    )
    
    print(f"✅ Agent created successfully!")
    print(f"   Agent ID: {agent.id}")
    
    return agent

def create_sample_industrial_data():
    """
    Creates sample industrial data files for demonstration purposes.
    
    Returns:
        dict: Dictionary containing file paths and descriptions
    """
    print("\n📄 Creating sample industrial data files...")
    
    # Sample manufacturing data
    manufacturing_data = """Date,Shift,Line,Units_Produced,Target_Units,Downtime_Minutes,Quality_Pass_Rate,Energy_Consumption_kWh
2024-01-01,Day,Line_A,1250,1300,45,98.2,450
2024-01-01,Day,Line_B,980,1000,30,96.8,380
2024-01-01,Night,Line_A,1180,1300,60,97.5,420
2024-01-01,Night,Line_B,920,1000,25,98.1,360
2024-01-02,Day,Line_A,1320,1300,15,99.1,460
2024-01-02,Day,Line_B,1050,1000,20,97.9,390
2024-01-02,Night,Line_A,1200,1300,40,98.4,430
2024-01-02,Night,Line_B,990,1000,35,96.5,370
2024-01-03,Day,Line_A,1280,1300,25,98.7,455
2024-01-03,Day,Line_B,1020,1000,15,98.9,385
2024-01-03,Night,Line_A,1150,1300,70,96.8,415
2024-01-03,Night,Line_B,950,1000,45,97.2,365
2024-01-04,Day,Line_A,1310,1300,20,99.3,465
2024-01-04,Day,Line_B,1080,1000,10,99.1,395
2024-01-04,Night,Line_A,1220,1300,35,98.1,435
2024-01-04,Night,Line_B,980,1000,30,97.8,375
2024-01-05,Day,Line_A,1290,1300,30,98.5,450
2024-01-05,Day,Line_B,1040,1000,25,98.3,390
2024-01-05,Night,Line_A,1190,1300,50,97.7,425
2024-01-05,Night,Line_B,970,1000,40,96.9,370"""

    # Equipment sensor data
    sensor_data = """Timestamp,Equipment_ID,Temperature_C,Vibration_mm_s,Pressure_Bar,RPM,Status
2024-01-01 08:00:00,PUMP_001,45.2,2.1,8.5,1750,Normal
2024-01-01 08:15:00,PUMP_001,46.8,2.3,8.4,1748,Normal
2024-01-01 08:30:00,PUMP_001,48.1,2.6,8.3,1745,Normal
2024-01-01 08:45:00,PUMP_001,52.3,3.2,8.1,1740,Warning
2024-01-01 09:00:00,PUMP_001,55.8,4.1,7.9,1735,Warning
2024-01-01 09:15:00,PUMP_001,49.2,2.8,8.2,1742,Normal
2024-01-01 09:30:00,PUMP_001,47.5,2.4,8.4,1746,Normal
2024-01-01 08:00:00,MOTOR_002,78.5,1.8,0,2950,Normal
2024-01-01 08:15:00,MOTOR_002,82.1,2.1,0,2948,Normal
2024-01-01 08:30:00,MOTOR_002,85.3,2.4,0,2945,Normal
2024-01-01 08:45:00,MOTOR_002,89.7,3.1,0,2940,Warning
2024-01-01 09:00:00,MOTOR_002,94.2,4.5,0,2935,Critical
2024-01-01 09:15:00,MOTOR_002,81.8,2.2,0,2947,Normal
2024-01-01 09:30:00,MOTOR_002,79.3,1.9,0,2949,Normal"""

    # Quality control data
    quality_data = """Product_ID,Batch,Dimension_1_mm,Dimension_2_mm,Weight_g,Surface_Finish,Pass_Fail
P001_001,B2024001,25.02,15.98,127.5,8.2,Pass
P001_002,B2024001,24.98,16.01,128.1,8.4,Pass
P001_003,B2024001,25.05,15.95,127.8,8.1,Pass
P001_004,B2024001,24.92,16.08,129.2,7.9,Fail
P001_005,B2024001,25.01,15.99,127.9,8.3,Pass
P001_006,B2024002,24.99,16.02,128.0,8.5,Pass
P001_007,B2024002,25.03,15.97,127.6,8.2,Pass
P001_008,B2024002,24.95,16.05,128.4,7.8,Fail
P001_009,B2024002,25.00,16.00,127.7,8.4,Pass
P001_010,B2024002,25.04,15.96,127.3,8.1,Pass
P001_011,B2024003,24.97,16.03,128.2,8.3,Pass
P001_012,B2024003,25.02,15.98,127.8,8.0,Pass
P001_013,B2024003,24.93,16.07,129.1,7.7,Fail
P001_014,B2024003,25.01,15.99,127.5,8.2,Pass
P001_015,B2024003,25.00,16.01,128.0,8.4,Pass"""

    # Create data files
    sample_files = {
        "manufacturing_kpis.csv": {
            "content": manufacturing_data,
            "description": "Manufacturing KPI data including production targets, downtime, and quality metrics"
        },
        "equipment_sensors.csv": {
            "content": sensor_data,
            "description": "Equipment sensor data for predictive maintenance analysis"
        },
        "quality_control.csv": {
            "content": quality_data,
            "description": "Quality control measurements and pass/fail results"
        }
    }
    
    created_files = {}
    for filename, file_info in sample_files.items():
        file_path = f"/tmp/{filename}"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_info['content'])
        created_files[filename] = {
            "path": file_path,
            "description": file_info['description']
        }
        print(f"   Created: {filename}")
    
    print(f"✅ Successfully created {len(created_files)} sample data files")
    return created_files

def demonstrate_code_interpreter_capabilities(agent):
    """
    Demonstrate Code Interpreter capabilities with predefined analysis tasks.
    
    Args:
        agent: The agent with Code Interpreter capabilities
    """
    print("\n🎯 Demonstrating Code Interpreter Capabilities")
    print("=" * 55)
    
    # Create sample data files
    sample_files = create_sample_industrial_data()
    
    # Predefined analysis requests that showcase different capabilities
    demo_tasks = [
        {
            "task": "Load and analyze the manufacturing KPI data. Calculate Overall Equipment Effectiveness (OEE) and create a visualization.",
            "file": "manufacturing_kpis.csv"
        },
        {
            "task": "Analyze the equipment sensor data for anomaly detection. Create a time series plot showing temperature and vibration trends.",
            "file": "equipment_sensors.csv"
        },
        {
            "task": "Perform quality control analysis. Calculate process capability statistics and create a control chart.",
            "file": "quality_control.csv"
        }
    ]
    
    # Create a conversation thread for the demo
    thread = project.agents.threads.create()
    
    for i, demo in enumerate(demo_tasks, 1):
        print(f"\n{i}. 📊 Analysis Task: {demo['task']}")
        print(f"   📁 Using file: {demo['file']}")
        print("   💻 Agent is writing and executing code...")
        
        try:
            # Upload the data file first
            file_path = sample_files[demo['file']]['path']
            with open(file_path, 'rb') as file_stream:
                uploaded_file = project.agents.upload_file(
                    file_stream=file_stream,
                    purpose="assistants",
                    filename=demo['file']
                )
            
            # Create message with task and file reference
            message_content = f"{demo['task']}\n\nI've uploaded the file '{demo['file']}' for analysis."
            
            project.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=message_content,
                attachments=[{
                    "file_id": uploaded_file.id,
                    "tools": [{"type": "code_interpreter"}]
                }]
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
                        print(f"   🤖 Analysis Results:")
                        for content in message.content:
                            if hasattr(content, 'text'):
                                # Show truncated response for demo
                                text = content.text.value
                                if len(text) > 500:
                                    text = text[:500] + "...\n   [Output truncated for demo]"
                                print(f"   {text}")
                            
                            # Check for generated files/images
                            if hasattr(content, 'image_file'):
                                print(f"   📊 Generated visualization: {content.image_file.file_id}")
                        break
            else:
                print(f"   ❌ Failed: {run.status}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Brief pause between tasks
        time.sleep(2)
    
    # Cleanup sample files
    for file_info in sample_files.values():
        try:
            os.remove(file_info['path'])
        except:
            pass

def interactive_data_analysis(agent):
    """
    Start an interactive data analysis session with the agent.
    
    Args:
        agent: The agent with Code Interpreter capabilities
    """
    print("\n💻 Starting interactive data analysis session")
    print("=" * 60)
    print("You can ask the agent to:")
    print("• Analyze data and create visualizations")
    print("• Perform statistical calculations")
    print("• Generate reports and summaries")
    print("• Process files and create downloadable outputs")
    print("• Write and execute custom Python code")
    print("\nExample requests:")
    print("• 'Calculate the correlation between temperature and vibration'")
    print("• 'Create a histogram of production efficiency'")
    print("• 'Generate a trend analysis for the last 30 days'")
    print("• 'Build a simple predictive model for equipment failure'")
    print("\nType 'quit' to exit the session")
    print("=" * 60)
    
    # Create a conversation thread
    thread = project.agents.threads.create()
    
    while True:
        # Get user request
        user_request = input("\n📊 Your analysis request: ").strip()
        
        if user_request.lower() in ['quit', 'exit', 'bye']:
            print("\n👋 Thank you for using the Industrial Data Analyst!")
            break
        
        if not user_request:
            continue
        
        try:
            print("\n💻 Agent is processing your request...")
            
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
                        print(f"\n🤖 Data Analyst:")
                        for content in message.content:
                            if hasattr(content, 'text'):
                                print(content.text.value)
                            
                            # Show generated files/visualizations
                            if hasattr(content, 'image_file'):
                                print(f"\n📊 Generated visualization (File ID: {content.image_file.file_id})")
                        break
            else:
                print(f"❌ Analysis failed with status: {run.status}")
                
        except Exception as e:
            print(f"❌ Error processing request: {str(e)}")

# 5. Main Execution Flow
# ---------------------------------------------------------------------
def main():
    """
    Main function demonstrating Code Interpreter agent capabilities.
    """
    print("🏭 Industrial Data Analyst with Code Interpreter")
    print("=" * 60)
    print("This example demonstrates how to create an AI agent that can:")
    print("• Write and execute Python code in a secure environment")
    print("• Analyze industrial data and generate insights")
    print("• Create professional visualizations and charts")
    print("• Perform statistical analysis and calculations")
    print("• Process data files and generate reports")
    print("=" * 60)
    
    try:
        # Create the agent with Code Interpreter capabilities
        agent = create_data_analysis_agent()
        
        # Demonstrate capabilities with predefined tasks
        demonstrate_code_interpreter_capabilities(agent)
        
        # Start interactive analysis session
        interactive_data_analysis(agent)
        
    except Exception as e:
        print(f"❌ Error in main execution: {str(e)}")
        print("💡 Make sure your Azure AI Foundry credentials are properly configured")

if __name__ == "__main__":
    main()

# 6. Key Concepts and Best Practices
# ---------------------------------------------------------------------
# Code Interpreter Tool Benefits:
# • Secure Python execution environment (sandbox)
# • Access to popular data science libraries
# • File upload and processing capabilities  
# • Automatic session state management
# • Generated files can be downloaded
# • No infrastructure management required
#
# Best Practices for Code Interpreter:
# • Provide clear, specific instructions for code tasks
# • Use appropriate data visualization libraries
# • Handle errors gracefully in generated code
# • Validate data quality before analysis
# • Include proper documentation in generated code
# • Test with various data sizes and formats
#
# Industrial Use Cases:
# • Manufacturing KPI dashboards
# • Equipment performance analysis
# • Quality control statistical analysis
# • Predictive maintenance modeling
# • Production optimization studies
# • Energy efficiency analysis
# • Supply chain data analysis
# ---------------------------------------------------------------------