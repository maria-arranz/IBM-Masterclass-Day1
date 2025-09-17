# 🔗 Challenge 3: Connecting to External Tools with MCP

<div align="center">

![Challenge 3](https://img.shields.io/badge/Challenge-3-blue?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Difficulty-Intermediate-yellow?style=for-the-badge)
![Time](https://img.shields.io/badge/Time-25%20minutes-orange?style=for-the-badge)

**Connect your AI agent to external tools and services using Model Context Protocol!**

</div>

---

## 🎯 **Objective**

Transform the `ex3-s3-AgentWithMCP.py` example into a versatile agent that can connect to different external tools and data sources. Learn how to expand your AI agent's capabilities beyond custom functions by integrating with real external services!

## ✨ **What You'll Learn**

<table>
<tr>
<td>

### 🔄 **Core Skills**
- Model Context Protocol (MCP) integration
- External tool configuration and approval
- Managing agent-tool interactions
- Working with different data sources

</td>
<td>

### 🧠 **AI Concepts**  
- Tool orchestration and coordination
- External service integration patterns
- Security and approval workflows
- Scalable agent architecture

</td>
</tr>
</table>

---

## 📝 **Challenge Description**

Based on the example `ex3-s3-AgentWithMCP.py`, create an agent that can connect to multiple external tools and handle various data analysis tasks:

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin: 15px 0; color: white;">

### 🎯 **Your Mission**

1. **📊 Connect to GitHub repositories** for code analysis and documentation
2. **🔍 Explore different MCP servers** to understand available tools
3. **📝 Create interactive queries** that utilize external data sources
4. **⚙️ Handle tool approvals** and security considerations
5. **🎛️ Build a multi-tool workflow** that combines different external services

**🌟 Goal**: Create an agent that can seamlessly work with external tools to provide rich, data-driven responses!

</div>

---

## 📋 **Technical Requirements**

### 🥇 **Basic Level (20-25 minutes)** ✅ MAIN GOAL

<div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; margin: 10px 0;">

**Perfect for learning MCP fundamentals!**

- [ ] ✅ **GitHub Repository Connection**: Successfully connect to a GitHub repo using MCP
- [ ] ✅ **Documentation Analysis**: Ask the agent to summarize README files or documentation
- [ ] ✅ **Code Exploration**: Request information about specific files or project structure
- [ ] ✅ **Tool Approval Handling**: Understand and manage the approval workflow

</div>

### 🌟 **Advanced Level (Extra 10 minutes for fast finishers)** ⭐ BONUS

<div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 10px 0;">

**For those who want to explore multiple tools!**

- [ ] 🔥 **Multiple Repository Analysis**: Compare different GitHub repositories
- [ ] 🔥 **Custom Headers Configuration**: Set up authentication headers for private repos
- [ ] 🔥 **Error Handling**: Gracefully handle connection failures and tool errors
- [ ] 🔥 **Workflow Automation**: Create a multi-step analysis using different tools

</div>

---

## 💡 **Getting Started Hints**

### 🟢 **Basic Level Implementation**

<details>
<summary>🔍 <strong>Click to see MCP server options</strong></summary>

```python
# Different MCP servers you can try:
github_servers = {
    "azure_specs": "https://gitmcp.io/Azure/azure-rest-api-specs",
    "microsoft_docs": "https://gitmcp.io/MicrosoftDocs/azure-docs", 
    "pytorch": "https://gitmcp.io/pytorch/pytorch",
    "tensorflow": "https://gitmcp.io/tensorflow/tensorflow",
    "react": "https://gitmcp.io/facebook/react"
}

# Server labels for easy reference
server_labels = {
    "azure": "azure-specs",
    "docs": "microsoft-docs", 
    "pytorch": "pytorch-ml",
    "tensorflow": "tensorflow-ml",
    "react": "react-ui"
}
```

</details>

<details>
<summary>🎯 <strong>Sample Questions to Try</strong></summary>

**Basic Repository Analysis:**
- "Can you summarize the main README file for this repository?"
- "What is the purpose and main features of this project?"
- "List the main directories and their purposes"
- "What programming languages are used in this project?"

**Code Exploration:**
- "Find examples of how to use the main API"
- "What are the key configuration files in this repository?"
- "Show me the project's contributing guidelines"
- "What dependencies does this project have?"

</details>

<details>
<summary>🚀 <strong>Tool Configuration Examples</strong></summary>

```python
# Basic MCP tool setup
def setup_mcp_tool(server_url, label):
    mcp_tool = McpTool(
        server_label=label,
        server_url=server_url,
        allowed_tools=[],  # Allow all tools or specify specific ones
    )
    return mcp_tool

# Advanced configuration with headers
def setup_authenticated_mcp_tool(server_url, label, auth_token):
    mcp_tool = McpTool(
        server_label=label,
        server_url=server_url,
        allowed_tools=[],
    )
    mcp_tool.update_headers("Authorization", f"Bearer {auth_token}")
    return mcp_tool
```

</details>

---

### 🟡 **Advanced Level Implementation**

<details>
<summary>⚡ <strong>Multi-Repository Analysis</strong></summary>

```python
# Function to switch between different repositories
def analyze_multiple_repos(repos_config):
    """
    Analyze multiple repositories and compare them
    
    :param repos_config: Dictionary with repo URLs and labels
    """
    results = {}
    for repo_name, config in repos_config.items():
        # Set up MCP tool for each repository
        mcp_tool = setup_mcp_tool(config['url'], config['label'])
        # Perform analysis...
        results[repo_name] = analyze_repository(mcp_tool)
    return results

# Example configuration
repos_to_compare = {
    "pytorch": {
        "url": "https://gitmcp.io/pytorch/pytorch",
        "label": "pytorch-ml"
    },
    "tensorflow": {
        "url": "https://gitmcp.io/tensorflow/tensorflow", 
        "label": "tensorflow-ml"
    }
}
```

</details>

<details>
<summary>🔥 <strong>Advanced Analysis Workflows</strong></summary>

**Complex Multi-Step Analysis:**
- "Compare the README files of PyTorch and TensorFlow repositories"
- "Find all the configuration files across different repositories and summarize their purposes"
- "Analyze the project structure differences between React and similar UI frameworks"
- "Create a comparison report of documentation quality across multiple projects"

</details>

---

## 🔧 **Implementation Guide**

### **Step 1: Choose Your Repository**
Start with a well-documented repository like Azure specs or Microsoft docs for easier analysis.

### **Step 2: Set Up MCP Connection**
Configure the MCP tool with the repository URL and appropriate label.

### **Step 3: Test Basic Queries**
Start with simple questions about README files and project structure.

### **Step 4: Handle Approvals**
Understand the tool approval workflow and how to manage it programmatically.

### **Step 5: Expand to Multiple Tools**
Once comfortable, try connecting to different repositories and comparing results.

---

## 🎯 **Success Criteria**

### ✅ **You'll know you've succeeded when:**

**Basic Level:**
- Your agent can successfully connect to GitHub repositories via MCP
- Tool approval workflow works correctly
- Agent can answer questions about repository structure and documentation
- Error handling provides meaningful feedback

**Advanced Level:**
- Multiple repository connections work seamlessly
- Complex multi-step analyses complete successfully
- Custom authentication and headers are properly configured
- Your agent can compare and contrast different projects

---

## 🆘 **Common Issues & Solutions**

<details>
<summary>❗ <strong>MCP Connection Failures</strong></summary>

**Problem**: Agent can't connect to MCP server

**Solutions**:
- Verify the server URL is correct and accessible
- Check internet connectivity
- Ensure the MCP server is currently available
- Try a different repository if one is down

</details>

<details>
<summary>❗ <strong>Tool Approval Issues</strong></summary>

**Problem**: Tool calls are not being approved properly

**Solutions**:
- Check the approval workflow in your code
- Ensure `ToolApproval` objects are created correctly
- Verify headers are set if authentication is required
- Consider using `set_approval_mode("never")` for testing

</details>

<details>
<summary>❗ <strong>No Tool Responses</strong></summary>

**Problem**: Agent doesn't receive responses from external tools

**Solutions**:
- Check if `allowed_tools` list is too restrictive
- Verify the tool call format matches expected parameters
- Ensure proper error handling for failed tool calls
- Check the run status and error messages

</details>

---

## 🏆 **Bonus Challenges**

If you finish everything and want more:

1. **🔐 Authentication Mastery**: Set up connections to private repositories using proper authentication
2. **📊 Data Visualization**: Create summaries and reports from multiple repository analyses
3. **🎯 Smart Filtering**: Configure specific tools for different types of analysis
4. **🔄 Dynamic Switching**: Allow users to switch between different repositories in the same conversation

---

## 📚 **Key Learning Outcomes**

By completing this challenge, you'll understand:

- How Model Context Protocol (MCP) extends AI agent capabilities
- Best practices for external tool integration and security
- How to handle asynchronous tool approvals and workflows
- The power of connecting AI agents to real-world data sources

**🎉 Ready to connect your agent to the wider world? Let's build something amazing!**

---

<div align="center">

**💡 Remember**: MCP opens up infinite possibilities - start with simple queries and gradually build more complex workflows!

</div>