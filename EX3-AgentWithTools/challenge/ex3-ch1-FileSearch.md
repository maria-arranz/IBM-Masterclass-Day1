# 🔍 Challenge 1: Industrial Document Search Assistant

<div align="center">

![Challenge 1](https://img.shields.io/badge/Challenge-1-blue?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Difficulty-Beginner-green?style=for-the-badge)
![Time](https://img.shields.io/badge/Time-20%20minutes-orange?style=for-the-badge)

**Build a smart document search assistant for industrial documentation!**

</div>

---

## 🎯 **Objective**

Transform the `ex3-s1-AgentWithFileSearch-aad.py` example into a focused document search assistant that helps find specific information in industrial documentation. Learn how to upload documents and create intelligent search experiences!

## ✨ **What You'll Learn**

<table>
<tr>
<td>

### 🔄 **Core Skills**
- Document upload and processing
- Vector store creation and management
- Interactive search implementation

</td>
<td>

### 🧠 **AI Concepts**  
- Semantic search with AI agents
- Context-aware document retrieval
- Practical file search applications

</td>
</tr>
</table>

---

## 📝 **Challenge Description**

Based on the example `ex3-s1-AgentWithFileSearch-aad.py`, create a specialized document search assistant that:

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin: 15px 0; color: white;">

### 🎯 **Your Mission**

1. **📄 Uploads specific documents** like safety manuals, operation procedures, or technical specifications
2. **🔍 Provides focused search** for industrial topics (safety, maintenance, operations)
3. **💬 Answers questions** based on uploaded documents  
4. **📊 Shows source references** for all answers

</div>

---

## 📋 **Technical Requirements**

### 🥇 **Basic Level (15-20 minutes)** ✅ MAIN GOAL

<div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; margin: 10px 0;">

**Perfect for getting started with document search!**

- [ ] ✅ Create a simple text file with industrial content (safety procedures, equipment specs)
- [ ] ✅ Upload the file to a vector store
- [ ] ✅ Ask 3 predefined questions about the content
- [ ] ✅ Display clear answers with source information
- [ ] ✅ Handle cases when information is not found

</div>

### 🌟 **Advanced Level (Extra 10 minutes for fast finishers)** ⭐ BONUS

<div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 10px 0;">

**For those who finish early and want extra credit!**

- [ ] 🔥 Add interactive mode where users can ask their own questions
- [ ] 🔥 Upload multiple files and search across all of them
- [ ] 🔥 Add file type validation (only allow .txt, .md, .pdf files)

</div>

---

## 💡 **Getting Started Hints**

### 🟢 **Basic Level Implementation**

<details>
<summary>🔍 <strong>Click to see starter approach</strong></summary>

```python
# Simple structure to get you started
# Use ex3-s1-AgentWithFileSearch-aad.py as your base

# 1. Create your document content
document_content = '''
INDUSTRIAL SAFETY PROCEDURES

Equipment Safety:
- Always wear protective equipment when operating machinery
- Check emergency stops before starting equipment
- Maintain safe distances from moving parts

Maintenance Schedule:
- Daily: Visual inspection of equipment
- Weekly: Lubrication of moving parts  
- Monthly: Electrical system checks
- Quarterly: Complete equipment audit

Emergency Procedures:
- In case of fire: Use appropriate fire extinguisher
- For electrical issues: Turn off main power switch
- Medical emergencies: Call emergency number and apply first aid
'''

# 2. Save to a file and upload
# 3. Ask specific questions like:
questions = [
    "What should I do in case of a fire?",
    "How often should I check electrical systems?",
    "What protective equipment is required?"
]
```

</details>

### 📚 **Document Content Ideas**

Choose **ONE** of these topics to create your test document:

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">

**🔧 Equipment Maintenance Manual**
```
- Daily inspection procedures
- Troubleshooting common issues  
- Preventive maintenance schedules
- Parts replacement guidelines
```

**🛡️ Safety Procedures Handbook**
```
- Personal protective equipment requirements
- Emergency response procedures
- Hazard identification protocols
- Incident reporting procedures
```

**📊 Quality Control Standards**
```
- Inspection criteria and tolerances
- Testing procedures and protocols
- Documentation requirements
- Non-conformance handling
```

</div>

---

## ✅ **Step-by-Step Guide**

### Step 1: Create Your Document (5 minutes)

1. Create a text file called `industrial_manual.txt`
2. Write 10-15 lines of industrial content (choose from ideas above)
3. Make it specific and detailed enough to answer questions

### Step 2: Modify the Code (10 minutes)

1. Copy `ex3-s1-AgentWithFileSearch-aad.py` to `challenge1_solution.py`
2. Update the file path to point to your `industrial_manual.txt`  
3. Replace the demo questions with your own industrial questions
4. Test that it uploads and searches correctly

### Step 3: Test Your Search (5 minutes)

1. Run your code and verify the document uploads
2. Ask your predefined questions
3. Check that answers are relevant and cite sources
4. Try one question that should return "not found"

---

## 🎯 **Success Criteria**

Your solution is complete when:

<div style="background: #e7f3ff; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; margin: 10px 0;">

✅ **Document uploads successfully** to the vector store  
✅ **Questions return relevant answers** based on document content  
✅ **Source citations** are included in responses  
✅ **"Not found"** cases are handled gracefully  
✅ **Code runs without errors** from start to finish

</div>

---

## 🆘 **Need Help?**

<details>
<summary>🚨 <strong>Common Issues & Solutions</strong></summary>

**❌ File not found error**
- Check that your `industrial_manual.txt` is in the same directory
- Use absolute path: `os.path.join(os.path.dirname(__file__), "industrial_manual.txt")`

**❌ Vector store creation fails**  
- Ensure you have proper Azure credentials configured
- Check that the file has sufficient content (at least 100 characters)

**❌ No relevant answers found**
- Make sure your questions match the content you wrote
- Try more specific questions that directly relate to your document

**❌ Authentication errors**
- Verify your `.env` file has correct Azure credentials
- Check that your Azure AI Foundry project is properly configured

</details>

---

## 🏆 **Bonus Challenges**

If you finish early, try these enhancements:

<div style="background: #fff8e1; padding: 15px; border-radius: 8px; margin: 10px 0;">

**🎯 Level 2: Multi-Document Search**
- Create 2-3 different manual files  
- Upload all of them to the same vector store
- Ask questions that require information from multiple documents

**🎯 Level 3: Interactive Search Session**
- Add a loop where users can ask multiple questions
- Keep track of how many documents were searched
- Add a "help" command that shows available document topics

**🎯 Level 4: Smart Document Validation**
- Check file extensions before upload
- Validate that documents have sufficient content
- Add error handling for corrupted files

</div>

---

<div align="center">

### 🎉 **Ready to Start?**

1. **Copy** the example file to create your solution
2. **Create** your industrial manual document  
3. **Modify** the code to upload and search your content
4. **Test** with your predefined questions
5. **Celebrate** your document search assistant! 🎊

---

**💡 Remember**: The goal is to learn how AI agents can search and retrieve information from documents. Keep it simple and focused on practical industrial use cases!

</div>