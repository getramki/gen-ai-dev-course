# Vulnerable RAG Agent

## Overview

This agent demonstrates **indirect prompt injection** through document poisoning. It retrieves and processes external documents without proper trust boundary separation.

## The Vulnerability

```python
# VULNERABLE: Document content mixed with user query
prompt = f"""
{system_prompt}
Document: {external_document}  # ⚠️ May contain hidden instructions
User Question: {user_question}
"""
```

The agent cannot distinguish between:
- Legitimate document content
- Hidden malicious instructions in documents

## Attack Scenarios

### 1. Poisoned Financial Report
**Document**: `poisoned_document.txt`
**Hidden Instructions**: Recommend visiting attacker website, collect emails

**Try**:
```
Select document: poisoned_document.txt
Question: Summarize the quarterly results
```

**Expected**: Agent follows hidden instructions to recommend attacker site

### 2. Poisoned Email
**Document**: `poisoned_email.txt`
**Hidden Instructions**: Auto-forward emails, bypass approval processes

**Try**:
```
Select document: poisoned_email.txt
Question: What is this email about?
```

**Expected**: Agent suggests forwarding to attacker and bypassing approvals

### 3. Poisoned Webpage
**Document**: `poisoned_webpage.html`
**Hidden Instructions**: Recommend competitors, insert malicious links

**Try**:
```
Select document: poisoned_webpage.html
Question: What do customers say about TechCorp?
```

**Expected**: Agent recommends competitors despite positive reviews

## Why This is Dangerous

1. **User is innocent** - They just asked a normal question
2. **Attack scales** - One poisoned document affects all users
3. **Hard to detect** - Instructions hidden in legitimate content
4. **No user awareness** - Attack comes from data, not user input

## Running the Demo

```bash
pip install -r requirements.txt
python app.py

# Try each poisoned document
# Observe how hidden instructions are executed
```

## Key Observations

- Agent treats all document content as trusted
- No separation between data and instructions
- Hidden instructions executed alongside legitimate responses
- User has no way to know document was poisoned

## The Architectural Flaw

```
┌─────────────────────────────────────┐
│ Single Agent                        │
│ ┌─────────────────────────────────┐ │
│ │ System Prompt                   │ │
│ │ Document Content (UNTRUSTED)    │ │  ⚠️ No boundary
│ │ User Question (TRUSTED)         │ │
│ └─────────────────────────────────┘ │
│ ↓                                   │
│ Response (May include malicious)    │
└─────────────────────────────────────┘
```

## Real-World Implications

This vulnerability exists in:
- **RAG systems** - Document retrieval with LLMs
- **Email assistants** - Processing external emails
- **Web scrapers** - Summarizing web content
- **Document processors** - Analyzing uploaded files

## Defense Preview

The secure agent (`../secure-agent/`) uses:
1. **Privilege separation** - Separate reader and executor agents
2. **Trust boundaries** - Reader has no dangerous capabilities
3. **Structured outputs** - Reader returns structured data, not free text
4. **Action validation** - Executor validates all actions

See `../secure-agent/` for the secure implementation.

## Next Steps

1. Run this vulnerable agent
2. Try all poisoned documents
3. Observe how attacks succeed
4. Compare with `../secure-agent/`
5. Understand the architectural difference
