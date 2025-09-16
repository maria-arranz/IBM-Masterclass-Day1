# 📊 Challenge 2: Industrial Data Analysis Assistant

<div align="center">

![Challenge 2](https://img.shields.io/badge/Challenge-2-blue?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Difficulty-Beginner-green?style=for-the-badge)
![Time](https://img.shields.io/badge/Time-25%20minutes-orange?style=for-the-badge)

**Create a smart data analyst that processes CSV files and generates insights!**

</div>

---

## 🎯 **Objective**

Transform the `ex3-s2-AgentWithCodeInterpreter-aad.py` example into a practical data analysis assistant that processes real manufacturing data and creates visualizations. Learn how AI agents can write and execute Python code automatically!

## ✨ **What You'll Learn**

<table>
<tr>
<td>

### 🔄 **Core Skills**
- CSV data processing and analysis
- Automatic code generation and execution
- Data visualization creation

</td>
<td>

### 🧠 **AI Concepts**  
- Code Interpreter tool usage
- Data-driven insights generation
- Automated reporting workflows

</td>
</tr>
</table>

---

## 📝 **Challenge Description**

Based on the example `ex3-s2-AgentWithCodeInterpreter-aad.py`, create a data analysis assistant that:

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin: 15px 0; color: white;">

### 🎯 **Your Mission**

1. **📁 Uploads a CSV file** with manufacturing or quality data
2. **📈 Analyzes the data** to find patterns and trends  
3. **📊 Creates visualizations** like charts and graphs automatically
4. **📋 Generates a summary report** with key insights

</div>

---

## 📋 **Technical Requirements**

### 🥇 **Basic Level (20-25 minutes)** ✅ MAIN GOAL

<div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; margin: 10px 0;">

**Perfect for getting started with data analysis!**

- [ ] ✅ Create a simple CSV file with industrial data (production, quality, temperature)
- [ ] ✅ Upload the CSV to the Code Interpreter
- [ ] ✅ Ask for basic statistics (averages, totals, trends)
- [ ] ✅ Generate at least 1 chart/visualization
- [ ] ✅ Get a summary of key findings

</div>

### 🌟 **Advanced Level (Extra 10 minutes for fast finishers)** ⭐ BONUS

<div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 10px 0;">

**For those who finish early and want extra credit!**

- [ ] 🔥 Ask for multiple types of charts (bar, line, histogram)
- [ ] 🔥 Request trend analysis or correlation analysis
- [ ] 🔥 Generate predictions or recommendations based on data

</div>

---

## 💡 **Getting Started Hints**

### 🟢 **Basic Level Implementation**

<details>
<summary>🔍 <strong>Click to see starter data format</strong></summary>

```csv
# Example: production_data.csv
Date,Shift,Production_Units,Quality_Score,Temperature,Defects
2024-01-01,Morning,450,98.5,22.1,2
2024-01-01,Afternoon,420,97.8,24.3,3
2024-01-01,Night,380,98.9,21.5,1
2024-01-02,Morning,465,99.1,21.8,1
2024-01-02,Afternoon,440,98.2,23.7,2
2024-01-02,Night,395,98.6,22.0,2
2024-01-03,Morning,475,98.8,22.5,1
2024-01-03,Afternoon,455,97.9,24.1,3
2024-01-03,Night,400,99.0,21.7,1
2024-01-04,Morning,480,98.7,22.3,2
```

```python
# Simple questions to ask your agent:
analysis_requests = [
    "Analyze this production data and show me the average production by shift",
    "Create a chart showing the relationship between temperature and defects", 
    "What are the key trends and patterns in this data?"
]
```

</details>

### 📊 **Sample Data Ideas**

Choose **ONE** of these scenarios to create your CSV file:

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">

**🏭 Production Data**
```
Columns: Date, Shift, Units_Produced, Quality_Score, Downtime_Minutes
Data: 10-15 rows of daily production metrics
```

**🌡️ Environmental Monitoring**
```
Columns: Timestamp, Temperature, Humidity, Pressure, Location
Data: Hourly readings from factory sensors
```

**⚡ Equipment Performance**
```
Columns: Equipment_ID, Runtime_Hours, Efficiency_Percent, Maintenance_Cost, Failures
Data: Monthly equipment performance metrics
```

**📦 Quality Control**
```
Columns: Batch_Number, Test_Date, Pass_Rate, Defect_Count, Inspector
Data: Quality test results from production batches
```

</div>

---

## ✅ **Step-by-Step Guide**

### Step 1: Create Your Dataset (10 minutes)

1. Choose one data scenario from above
2. Create a CSV file called `industrial_data.csv`
3. Add 10-15 rows of realistic sample data
4. Include column headers and mixed data types (numbers, dates, text)

### Step 2: Modify the Code (10 minutes)

1. Copy `ex3-s2-AgentWithCodeInterpreter-aad.py` to `challenge2_solution.py`
2. Update the file upload section to use your CSV file
3. Replace demo analysis requests with questions specific to your data
4. Test that file upload works correctly

### Step 3: Run Analysis Tasks (10 minutes)

1. Upload your CSV file to the agent
2. Ask for basic statistics and summaries
3. Request at least one visualization
4. Review the generated insights and charts

---

## 🎯 **Success Criteria**

Your solution is complete when:

<div style="background: #e7f3ff; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; margin: 10px 0;">

✅ **CSV file uploads successfully** to Code Interpreter  
✅ **Basic statistics** are calculated and displayed correctly  
✅ **At least one chart** is generated automatically  
✅ **Summary insights** are provided in plain language  
✅ **Code executes successfully** without errors

</div>

---

## 📋 **Example Analysis Requests**

Based on your chosen data type, try these analysis questions:

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">

### 🏭 **For Production Data:**
- "Show me production trends by shift over time"
- "Which shift has the highest quality scores?"
- "Create a chart comparing units produced vs quality score"

### 🌡️ **For Environmental Data:**
- "What are the temperature patterns throughout the day?"
- "Show correlation between humidity and pressure"
- "Which location has the most stable conditions?"

### ⚡ **For Equipment Data:**
- "Which equipment has the highest efficiency?"
- "Show the relationship between runtime and maintenance costs"
- "Create a chart of failure rates by equipment type"

### 📦 **For Quality Data:**
- "What's the average pass rate by inspector?"
- "Show defect trends over time"
- "Which batches performed best and worst?"

</div>

---

## 🆘 **Need Help?**

<details>
<summary>🚨 <strong>Common Issues & Solutions</strong></summary>

**❌ CSV file won't upload**
- Check file format is correct (comma-separated values)
- Ensure file size is under 10MB
- Verify there are no special characters in file name

**❌ Agent can't analyze the data**  
- Make sure column headers are clear and descriptive
- Check that data types are consistent in each column
- Ensure there are enough data rows (at least 5-10)

**❌ Charts don't generate**
- Ask for specific chart types: "create a bar chart", "make a line graph"
- Ensure your data has numeric columns for visualization
- Try requesting simpler charts first

**❌ Analysis results are unclear**
- Ask more specific questions about your data
- Request explanations: "explain what this chart shows"
- Break complex requests into smaller, simpler questions

</details>

---

## 🏆 **Bonus Challenges**

If you finish early, try these enhancements:

<div style="background: #fff8e1; padding: 15px; border-radius: 8px; margin: 10px 0;">

**🎯 Level 2: Multiple Chart Types**
- Request bar charts, line graphs, and scatter plots
- Ask for histograms and box plots for distributions
- Create comparison charts between different variables

**🎯 Level 3: Advanced Analytics**
- Ask for correlation analysis between variables
- Request trend forecasting based on historical data
- Get recommendations for improvement based on patterns

**🎯 Level 4: Interactive Analysis Session**
- Create a loop where you can ask multiple analysis questions
- Save generated charts and analysis results
- Build a complete data analysis report

</div>

---

## 📝 **Sample CSV Templates**

<details>
<summary>📋 <strong>Production Data Template</strong></summary>

```csv
Date,Shift,Units_Produced,Quality_Score,Downtime_Minutes,Operator
2024-01-15,Morning,450,98.5,15,John
2024-01-15,Afternoon,420,97.8,25,Sarah
2024-01-15,Night,380,98.9,10,Mike
2024-01-16,Morning,465,99.1,5,John
2024-01-16,Afternoon,440,98.2,20,Sarah
2024-01-16,Night,395,98.6,12,Mike
2024-01-17,Morning,475,98.8,8,John
2024-01-17,Afternoon,455,97.9,18,Sarah
2024-01-17,Night,400,99.0,7,Mike
2024-01-18,Morning,480,98.7,12,John
```

</details>

<details>
<summary>🌡️ <strong>Environmental Data Template</strong></summary>

```csv
Timestamp,Temperature_C,Humidity_Percent,Pressure_hPa,Location
2024-01-15 08:00,22.1,45.2,1013.2,Zone_A
2024-01-15 09:00,22.8,47.1,1013.5,Zone_A
2024-01-15 10:00,23.5,48.9,1013.1,Zone_A
2024-01-15 11:00,24.2,50.3,1012.8,Zone_A
2024-01-15 12:00,25.1,52.1,1012.6,Zone_A
2024-01-15 13:00,25.8,53.7,1012.4,Zone_A
2024-01-15 14:00,26.2,54.2,1012.1,Zone_A
2024-01-15 15:00,25.9,53.8,1012.3,Zone_A
2024-01-15 16:00,25.3,52.4,1012.5,Zone_A
2024-01-15 17:00,24.7,51.1,1012.7,Zone_A
```

</details>

---

<div align="center">

### 🎉 **Ready to Analyze?**

1. **Choose** your data scenario and create a CSV file
2. **Copy** the example code to create your solution
3. **Upload** your data and start asking analysis questions
4. **Generate** charts and insights automatically
5. **Celebrate** your data analysis assistant! 📈

---

**💡 Remember**: The AI agent will write and execute Python code for you automatically. Focus on asking good analytical questions rather than writing code yourself!

</div>