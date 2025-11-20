# Module 1: Exercises - MCP Fundamentals

## Exercise 1: Understanding MCP Components (15 minutes)

### Objective
Identify and understand the role of each MCP component in a real-world scenario.

### Scenario
You're building an AI assistant that needs to:
- Check weather information
- Read files from a local directory
- Send emails

### Task
Map each requirement to MCP components:

1. **Weather Information**: 
   - Component: ________________
   - Type: ________________
   - Why: ________________

2. **File Reading**:
   - Component: ________________
   - Type: ________________
   - Why: ________________

3. **Email Sending**:
   - Component: ________________
   - Type: ________________
   - Why: ________________

### Solution
Check `solutions/exercise-1-solution.md` for answers.

## Exercise 2: MCP Message Analysis (15 minutes)

### Objective
Analyze different MCP message types and understand their structure.

### Given Messages
Examine these MCP messages and identify their types:

**Message A:**
```json
{
  "name": "database_query",
  "description": "Execute SQL queries on the database",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "database": {"type": "string"}
    },
    "required": ["query"]
  }
}
```

**Message B:**
```json
{
  "uri": "postgres://localhost:5432/users",
  "name": "User Database",
  "description": "Customer user database",
  "mimeType": "application/sql"
}
```

**Message C:**
```json
{
  "name": "email_template",
  "description": "Generate professional email template",
  "arguments": [
    {"name": "recipient", "description": "Email recipient name"},
    {"name": "subject", "description": "Email subject"},
    {"name": "tone", "description": "Email tone (formal/casual)"}
  ]
}
```

### Tasks
1. Identify the type of each message (Tool/Resource/Prompt)
2. Explain what each message enables
3. Suggest improvements for each message

### Your Analysis
**Message A Type**: ________________
**Message A Purpose**: ________________

**Message B Type**: ________________
**Message B Purpose**: ________________

**Message C Type**: ________________
**Message C Purpose**: ________________

## Exercise 3: Design Your First MCP Server (15 minutes)

### Objective
Design an MCP server for a specific use case.

### Scenario
You need to create an MCP server for a "Personal Assistant" that helps with:
- Managing a to-do list
- Getting current time/date
- Converting units (temperature, distance, etc.)

### Tasks
1. **Server Name**: Choose a descriptive name
2. **Tools**: Design 3 tools with their schemas
3. **Resources**: Identify any resources needed
4. **Prompts**: Design 1 helpful prompt template

### Your Design

**Server Name**: ________________

**Tool 1 - To-Do Management**
```json
{
  "name": "________________",
  "description": "________________",
  "inputSchema": {
    // Your schema here
  }
}
```

**Tool 2 - Time/Date**
```json
{
  "name": "________________",
  "description": "________________",
  "inputSchema": {
    // Your schema here
  }
}
```

**Tool 3 - Unit Conversion**
```json
{
  "name": "________________",
  "description": "________________",
  "inputSchema": {
    // Your schema here
  }
}
```

**Resource 1**
```json
{
  "uri": "________________",
  "name": "________________",
  "description": "________________"
}
```

**Prompt Template**
```json
{
  "name": "________________",
  "description": "________________",
  "arguments": [
    // Your arguments here
  ]
}
```

## Bonus Challenge: MCP Flow Diagram

### Objective
Create a flow diagram showing how an MCP client interacts with a server.

### Scenario
Client wants to get weather information and then send an email with the weather report.

### Task
Draw or describe the step-by-step flow:

1. Step 1: ________________
2. Step 2: ________________
3. Step 3: ________________
4. Step 4: ________________
5. Step 5: ________________

## Reflection Questions

1. **What makes MCP different from regular APIs?**
   Your answer: ________________

2. **Why is the standardized protocol important?**
   Your answer: ________________

3. **How does MCP benefit AI applications?**
   Your answer: ________________

4. **What challenges might you face when implementing MCP?**
   Your answer: ________________

## Next Steps
- Review your answers with the solutions
- Prepare for Module 2: Environment Setup
- Think about what MCP server you'd like to build

**Time to Complete**: 45 minutes total
**Difficulty**: Beginner
**Prerequisites**: Basic understanding of APIs and JSON