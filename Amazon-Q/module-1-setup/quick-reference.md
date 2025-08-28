# Module 1 Quick Reference Guide

## Installation Commands

### VS Code
```
Extensions → Search "Amazon Q" → Install
```

### IntelliJ IDEA
```
File → Settings → Plugins → Search "Amazon Q" → Install
```

---

## Authentication Options

| Method | Best For | Steps |
|--------|----------|-------|
| AWS Builder ID | Individual developers | Email → Verification → Profile |
| IAM Identity Center | Enterprise users | Organization SSO |

---

## Basic Amazon Q Syntax

### Chat Commands
```
Hello Amazon Q
Write a Python function to [description]
Explain this code: [code snippet]
@filename.py [question about file]
```

### Keyboard Shortcuts
| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Trigger suggestions | Alt+C | Option+C |
| Open chat | Ctrl+Shift+P → "Amazon Q" | Cmd+Shift+P → "Amazon Q" |

---

## Interface Elements

### Chat Panel
- **Location:** Side panel or bottom panel
- **Purpose:** Conversational interactions
- **Features:** File context, multi-turn conversations

### Inline Suggestions
- **Appearance:** Grayed-out text while typing
- **Trigger:** Automatic or Alt+C/Option+C
- **Accept:** Tab key

### Status Indicators
- **Connection:** Green dot = Connected
- **Suggestions:** Available/Unavailable
- **Usage:** Token count (if shown)

---

## First Interaction Patterns

### Code Generation Requests
```
"Create a [language] function that [does something]"
"Write a [language] class for [purpose]"
"Generate a [type] algorithm for [problem]"
```

### Code Explanation Requests
```
"Explain this code"
"What does this function do?"
"How does this algorithm work?"
```

### File Context Usage
```
"@filename.py explain this file"
"@filename.py add a new method"
"@filename.py find bugs in this code"
```

---

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Not authenticated | Click Amazon Q icon → Sign in |
| No suggestions | Alt+C to trigger manually |
| Extension missing | Restart IDE, check Extensions |
| Chat not responding | Check internet, restart extension |

---

## Quality Indicators

### Good Amazon Q Response
- ✅ Syntactically correct code
- ✅ Follows language conventions
- ✅ Includes helpful comments
- ✅ Addresses the specific request

### When to Ask Follow-up
- ❓ Code doesn't compile
- ❓ Logic seems incorrect
- ❓ Need additional features
- ❓ Want explanation of approach

---

## Best Practices for Module 1

### Effective Prompting
1. Be specific about language and requirements
2. Provide context when needed
3. Ask follow-up questions for clarification
4. Use @filename for file-specific questions

### Testing Generated Code
1. Copy code to appropriate file
2. Check syntax highlighting
3. Run/compile to verify functionality
4. Test with sample inputs

### Building Context
1. Start with simple requests
2. Build complexity gradually
3. Reference previous responses
4. Use file context appropriately

---

## Module 1 Completion Checklist

- [ ] Amazon Q installed and authenticated
- [ ] Successfully generated hello world programs
- [ ] Used chat for code explanation
- [ ] Tested @filename file context
- [ ] Understand basic interface elements
- [ ] Ready for advanced features in Module 2

**Estimated Time:** 20 minutes  
**Difficulty Level:** Beginner  
**Success Rate:** Should be 100% with proper setup