# 🤖 Exercise 2: First Agent

<div align="center">

![Agent](https://img.shields.io/badge/AI-Agents-purple?style=for-the-badge&logo=robot)
![Azure](https://img.shields.io/badge/Azure-AI%20Foundry-0078D4?style=for-the-badge&logo=microsoft-azure)
![Difficulty](https://img.shields.io/badge/Difficulty-Beginner-green?style=for-the-badge)

**Create your first intelligent AI agent using Azure AI Foundry Agent Service**

</div>

---

## 🎯 **Objective**

Learn how to create and deploy your first AI agent using Azure AI Foundry, understanding the key differences between basic chat completions and intelligent agent architectures.

## ✨ **What You'll Learn**

<table>
<tr>
<td>

### 🤖 **Agent Fundamentals**
- AI Agent concepts and architecture
- Agent vs Chat Completion differences
- Agent lifecycle management
- Persistent conversation threads

</td>
<td>

### 🔐 **Authentication Methods**
- Azure Active Directory (AAD) integration
- Service Principal authentication
- Token-based security patterns
- Production authentication best practices

</td>
</tr>
</table>

---

## 📚 **Available Examples**

### 🔐 **Authentication Options**

We provide two authentication methods to suit different environments and security requirements:

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">

#### 🌟 **Option 1: Azure Default Credential (AAD) - Recommended for Development**

**Files:** `*-aad.py`

✅ **Best for:**
- Local development environments
- VS Code integration
- Azure CLI authenticated users
- Managed Identity scenarios

✅ **Advantages:**
- No need to manage secrets locally
- Automatic credential discovery
- Seamless Azure integration
- Multiple fallback methods

**Authentication flow:**
1. Environment variables → 2. Managed Identity → 3. VS Code → 4. Azure CLI

</div>

<div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 15px 0;">

#### 🔒 **Option 2: Service Principal (SP) - Recommended for Production**

**Files:** `*-sp.py`

✅ **Best for:**
- Production environments
- CI/CD pipelines
- Service-to-service authentication
- Fine-grained access control

✅ **Advantages:**
- Explicit credential management
- Enhanced security controls
- Audit trails and compliance
- Role-based access control (RBAC)

**Required credentials:**
- `AZURE_TENANT_ID` - Your Azure AD tenant ID
- `AZURE_CLIENT_ID` - Application (client) ID
- `AZURE_CLIENT_SECRET` - Client secret value

</div>

---

## 📁 **Sample Files**

### 🎯 **Core Agent Examples**

| File | Description | Auth Method |
|------|-------------|-------------|
| `ex2-s1-agentaiservice-aad.py` | Basic agent with AAD authentication | Azure Default Credential |
| `ex2-s1-agentaiservice-sp.py` | Basic agent with Service Principal | Client Secret Credential |
| `ex2-s2-agentChainlit-aad.py` | Agent + Chainlit web interface (AAD) | Azure Default Credential |
| `ex2-s2-agentChainlit-sp.py` | Agent + Chainlit web interface (SP) | Client Secret Credential |

### 🏆 **Challenge Projects**

| Challenge | Description | Level |
|-----------|-------------|-------|
| [Travel Companion Agent](./challenge/ex2-travel-companion-challenge.md) | Specialized travel advisor with memory | Beginner |

---

## 🛠️ **Prerequisites**

### ✅ **Completed Requirements**
- [EX1: FirstAIChat](../EX1-FirstAIChat/) successfully completed
- Basic understanding of Python async programming
- Familiarity with Azure services and authentication

### 🔧 **Azure Setup Requirements**
- Azure AI Foundry project configured
- Appropriate authentication method set up (see below)
- Model deployment available in your AI Foundry project

### 🔐 **Authentication Setup**

<details>
<summary><strong>🌟 Option 1: Azure Default Credential (Development)</strong></summary>

**For local development, use one of these methods:**

1. **Azure CLI (Recommended)**
   ```bash
   az login
   az account set --subscription "your-subscription-id"
   ```

2. **VS Code Azure Extension**
   - Install Azure Account extension
   - Sign in through VS Code

3. **Environment Variables**
   ```bash
   export AZURE_TENANT_ID="your-tenant-id"
   export AZURE_CLIENT_ID="your-client-id"
   export AZURE_CLIENT_SECRET="your-client-secret"
   ```

</details>

<details>
<summary><strong>🔒 Option 2: Service Principal (Production)</strong></summary>

**1. Create an App Registration in Azure Portal:**
   - Go to Azure Active Directory → App registrations
   - Click "New registration"
   - Note the Application (client) ID and Directory (tenant) ID

**2. Create a Client Secret:**
   - In your app registration, go to "Certificates & secrets"
   - Click "New client secret"
   - Copy the secret value immediately

**3. Assign Permissions:**
   - Add your service principal to the AI Foundry project
   - Assign appropriate roles (AI Developer, Contributor)

**4. Set Environment Variables:**
   ```bash
   export AZURE_TENANT_ID="your-tenant-id"
   export AZURE_CLIENT_ID="your-client-id"
   export AZURE_CLIENT_SECRET="your-client-secret"
   export AI_FOUNDRY_ENDPOINT="your-foundry-endpoint"
   export AI_FOUNDRY_DEPLOYMENT_NAME="your-model-deployment"
   ```

</details>

---

## 🚀 **Getting Started**

### 📝 **Step 1: Choose Your Authentication Method**

**For learning/development:** Start with AAD files (`*-aad.py`)
**For production setup:** Use Service Principal files (`*-sp.py`)

### 📝 **Step 2: Run Your First Agent**

```bash
# For basic agent interaction
python samples/ex2-s1-agentaiservice-aad.py

# For web interface
chainlit run samples/ex2-s2-agentChainlit-aad.py
```

### 📝 **Step 3: Try the Challenge**

Complete the [Travel Companion Challenge](./challenge/ex2-travel-companion-challenge.md) to build a specialized agent.

---

## 🔍 **Key Concepts**

### 🤖 **Agent vs Chat Completion**

<table>
<tr>
<th>Chat Completion</th>
<th>AI Agent</th>
</tr>
<tr>
<td>

- Stateless interactions
- Manual context management
- Single request/response
- No built-in memory

</td>
<td>

- Persistent conversations
- Automatic context management
- Thread-based interactions
- Built-in memory and state

</td>
</tr>
</table>

### 🧠 **Agent Architecture**

1. **Agent Creation** - Define personality and capabilities
2. **Thread Management** - Maintain conversation context
3. **Message Processing** - Handle user interactions
4. **Run Execution** - Process and generate responses
5. **State Persistence** - Remember conversation history

---

## 🔧 **Environment Variables**

```bash
# Azure AI Foundry Configuration
AI_FOUNDRY_ENDPOINT="https://your-project.region.ai.azure.com"
AI_FOUNDRY_DEPLOYMENT_NAME="your-model-deployment"

# Authentication (choose one method)

# Option 1: Service Principal
AZURE_TENANT_ID="your-tenant-id"
AZURE_CLIENT_ID="your-client-id" 
AZURE_CLIENT_SECRET="your-client-secret"

# Option 2: Azure Default Credential (uses Azure CLI/VS Code)
# No additional environment variables needed
```

---

## 🆘 **Troubleshooting**

<details>
<summary><strong>Authentication Issues</strong></summary>

**DefaultAzureCredential not working?**
- Ensure you're logged in via Azure CLI: `az login`
- Check your subscription: `az account show`
- Try VS Code Azure Account extension

**Service Principal issues?**
- Verify all three credentials are set correctly
- Check the service principal has appropriate permissions
- Ensure the client secret hasn't expired

</details>

<details>
<summary><strong>Agent Creation Failures</strong></summary>

**"Model deployment not found"**
- Verify `AI_FOUNDRY_DEPLOYMENT_NAME` matches your deployment
- Check the model is deployed and available
- Ensure you have access to the deployment

</details>

---

## 🌟 **What's Next?**

After completing this exercise, you'll be ready for:
- **EX3: AgentWithAISearch** - Enhance agents with search capabilities
- **EX4: AgentWithMCP** - Advanced context and memory management  
- **EX5-6: Agent Orchestration** - Multi-agent coordination patterns

---

<div align="center">

**🎯 Ready to build your first intelligent agent? Choose your authentication method and let's get started!**

</div>
