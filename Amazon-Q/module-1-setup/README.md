# Module 1: Getting Started with Amazon Q Developer

**Duration:** 20 minutes  
**Objective:** Install, configure, and make first interactions with Amazon Q Developer

---

## Topic 1.1: Introduction and Setup (10 minutes)

### What is Amazon Q Developer?

Amazon Q Developer is an AI-powered coding assistant that helps developers:
- Generate code from natural language descriptions
- Provide intelligent code completions
- Explain existing code
- Debug and optimize applications
- Ensure security best practices
- Generate documentation

### Prerequisites Checklist
- [ ] VS Code or IntelliJ IDEA installed
- [ ] AWS account created
- [ ] Internet connection
- [ ] Basic programming knowledge

### Installation Steps

#### For VS Code:
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Amazon Q"
4. Click "Install" on "Amazon Q" extension
5. Restart VS Code if prompted

#### For IntelliJ IDEA:
1. Open IntelliJ IDEA
2. Go to File → Settings → Plugins
3. Search for "Amazon Q"
4. Click "Install" and restart IDE

### Authentication Setup

1. After installation, you'll see Amazon Q icon in your IDE
2. Click on Amazon Q icon
3. Choose authentication method:
   - **AWS Builder ID** (Recommended for individual developers)
   - **IAM Identity Center** (For enterprise users)
4. Follow the browser authentication flow
5. Return to IDE once authenticated

### Verification
- Amazon Q chat panel should be available
- Status indicator shows "Connected"
- You can see Amazon Q suggestions in the status bar

---

## Topic 1.2: First Interactions (10 minutes)

### Understanding the Interface

#### Chat Panel
- Located in the side panel or bottom panel
- Used for conversational interactions
- Supports file context with @file syntax

#### Inline Suggestions
- Appear automatically while typing
- Triggered by Alt+C (Option+C on Mac)
- Show as grayed-out text completions

#### Status Indicators
- Connection status in status bar
- Suggestion availability indicators
- Usage metrics (if enabled)

### Basic Chat Functionality

#### Simple Queries
Try these basic interactions in the chat:
```
Hello, can you help me write code?
```

```
What programming languages do you support?
```

#### File Context
Use @file to include specific files:
```
@filename.py explain this code
```

### Workspace Awareness
Amazon Q understands your project structure and can:
- Reference multiple files
- Understand project dependencies
- Maintain context across conversations

---

## Hands-On Exercise 1.1: Installation and Authentication

### Task
Complete the installation and authentication process for Amazon Q Developer.

### Steps
1. Install Amazon Q extension in your IDE
2. Authenticate using AWS Builder ID
3. Verify the connection is successful
4. Take a screenshot of the successful setup

### Success Criteria
- [ ] Amazon Q extension installed
- [ ] Successfully authenticated
- [ ] Chat panel accessible
- [ ] Connection status shows "Connected"

---

## Hands-On Exercise 1.2: First Code Generation

### Task
Use Amazon Q to generate a simple "Hello World" program in your preferred language.

### Steps
1. Open Amazon Q chat panel
2. Type: "Create a hello world program in Python"
3. Copy the generated code to a new file
4. Run the program to verify it works

### Expected Output
```python
print("Hello, World!")
```

### Success Criteria
- [ ] Code generated successfully
- [ ] Code runs without errors
- [ ] Understanding of basic Amazon Q interaction

---

## Troubleshooting Common Issues

### Authentication Problems
- **Issue:** Can't authenticate with AWS Builder ID
- **Solution:** Check internet connection, try incognito browser mode

### Extension Not Loading
- **Issue:** Amazon Q extension not appearing
- **Solution:** Restart IDE, check extension is enabled

### No Suggestions Appearing
- **Issue:** Inline suggestions not showing
- **Solution:** Check Amazon Q is connected, try Alt+C to trigger manually

---

## Key Takeaways

After completing Module 1, you should:
- Have Amazon Q Developer installed and configured
- Understand the basic interface components
- Know how to interact with Amazon Q through chat
- Have generated your first piece of code
- Be ready to explore more advanced features

---

## Next Steps
Proceed to Module 2 to learn about intelligent code completion and generation from natural language descriptions.