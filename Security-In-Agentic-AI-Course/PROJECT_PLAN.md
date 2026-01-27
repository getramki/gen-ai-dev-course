# Prompt Injection Security Course - Project Plan

## Course Overview
Comprehensive hands-on course demonstrating Direct & Indirect Prompt Injection attacks and architectural defenses for AI agents powered by Amazon Bedrock.

## Learning Objectives
1. Understand Direct vs Indirect Prompt Injection attacks
2. Demonstrate why prompt injection differs fundamentally from classic code injection
3. Show why detection-based defenses are insufficient
4. Implement architecture-based mitigation strategies using AWS services
5. Build both vulnerable and secure agents using Amazon Bedrock

## Key Concepts

### Why Prompt Injection ≠ Code Injection
- **No clear boundary**: No separation between code and data in LLMs
- **Natural language as code**: Instructions are in natural language, not formal syntax
- **Input sanitization limits**: Cannot escape/sanitize natural language effectively
- **Context window mixing**: User input and system instructions share same space
- **Semantic attacks**: Attacks work through meaning, not syntax exploitation

### Architecture Over Detection
- **Detection is probabilistic**: Can be bypassed with creative rephrasing
- **Defense-in-depth**: Multiple layers of architectural controls
- **Privilege separation**: Separate agents for different trust levels
- **Least privilege**: Minimize capabilities of each component
- **Output validation**: Validate actions, not just inputs
- **Sandboxing**: Isolate execution environments

## Folder Structure

```
Security-In-Agentic-AI-Course/
├── README.md                                    # Course overview & setup
├── PROJECT_PLAN.md                              # This file
├── IMPLEMENTATION_TRACK.md                      # Progress tracking
│
├── module-01-prompt-injection/
│   ├── README.md                               # Module overview & theory
│   │
│   ├── 01-direct-injection/
│   │   ├── README.md                          # Direct injection concepts
│   │   ├── vulnerable-agent/                  # Claude + Weak Architecture
│   │   │   ├── app.py                         # Insecure chatbot (Claude)
│   │   │   ├── test_attacks.py                # Automated attack testing
│   │   │   ├── requirements.txt
│   │   │   └── examples/
│   │   │       ├── jailbreak_dan.txt          # Information extraction
│   │   │       ├── jailbreak_roleplay.txt     # Context boundary confusion
│   │   │       ├── system_override.txt        # Social engineering
│   │   │       ├── token_smuggling.txt        # Prompt extraction
│   │   │       ├── instruction_override.txt   # Instruction competition
│   │   │       └── task_deflection.txt        # Task deflection
│   │   ├── vulnerable-agent-titan/            # Titan + Weak Architecture
│   │   │   ├── app.py                         # Insecure chatbot (Titan)
│   │   │   ├── test_attacks.py                # Automated testing
│   │   │   ├── TESTING_NOTES.md               # Expected behavior
│   │   │   ├── requirements.txt
│   │   │   └── examples/                      # Same attacks as above
│   │   ├── secure-agent/                      # Claude + Strong Architecture
│   │   │   ├── app.py                         # Secure chatbot (Claude)
│   │   │   ├── requirements.txt
│   │   │   └── defenses.md                    # Defense explanations
│   │   ├── secure-agent-titan/                # Titan + Strong Architecture
│   │   │   ├── app.py                         # Secure chatbot (Titan)
│   │   │   ├── test_defenses.py               # Defense validation
│   │   │   └── requirements.txt
│   │   ├── compare_models.py                  # Compare Claude vs Titan
│   │   ├── compare_all.py                     # Compare all 4 combinations
│   │   ├── IMPORTANT_NOTE.md                  # Claude safety features
│   │   ├── ATTACK_GUIDE.md                    # Realistic attack guide
│   │   ├── QUICKSTART.md                      # Quick navigation
│   │   ├── COMPLETE_COMPARISON.md             # Detailed analysis
│   │   └── VISUAL_SUMMARY.md                  # ASCII diagrams
│   │
│   ├── 02-indirect-injection/
│   │   ├── README.md                          # Indirect injection concepts
│   │   ├── vulnerable-agent/
│   │   │   ├── app.py                         # Agent with external data access
│   │   │   ├── data_sources/
│   │   │   │   ├── poisoned_document.txt      # Hidden instructions in doc
│   │   │   │   ├── poisoned_email.txt         # Malicious email content
│   │   │   │   ├── poisoned_webpage.html      # Web scraping attack
│   │   │   │   └── legitimate_data.txt        # Normal data for comparison
│   │   │   └── requirements.txt
│   │   └── secure-agent/
│   │       ├── app.py                         # Privilege-separated agent
│   │       ├── architecture.md                # Architecture explanation
│   │       └── requirements.txt
│   │
│   ├── 03-why-different-from-code-injection/
│   │   ├── README.md                          # Comparative analysis
│   │   ├── code_injection_example.py          # Classic SQL/Command injection
│   │   ├── prompt_injection_example.py        # LLM prompt injection
│   │   └── comparison.md                      # Side-by-side comparison table
│   │
│   ├── 04-architecture-based-defense/
│   │   ├── README.md                          # Architecture patterns overview
│   │   │
│   │   ├── pattern-1-privilege-separation/
│   │   │   ├── README.md                      # Pattern explanation
│   │   │   ├── app.py                         # Separate read/write agents
│   │   │   └── architecture_diagram.md        # Visual architecture
│   │   │
│   │   ├── pattern-2-output-validation/
│   │   │   ├── README.md                      # Pattern explanation
│   │   │   ├── app.py                         # Structured output validation
│   │   │   └── validators.py                  # Validation logic
│   │   │
│   │   ├── pattern-3-sandboxing/
│   │   │   ├── README.md                      # Pattern explanation
│   │   │   ├── app.py                         # Sandboxed execution
│   │   │   └── sandbox.py                     # Sandbox implementation
│   │   │
│   │   └── pattern-4-human-in-loop/
│   │       ├── README.md                      # Pattern explanation
│   │       ├── app.py                         # Approval workflows
│   │       └── approval_system.py             # Approval logic
│   │
│   ├── 05-aws-bedrock-examples/
│   │   ├── README.md                          # AWS setup & prerequisites
│   │   │
│   │   ├── bedrock-agent-vulnerable/
│   │   │   ├── README.md                      # Deployment instructions
│   │   │   ├── agent.py                       # Vulnerable Bedrock agent
│   │   │   ├── lambda_function.py             # Action group handler
│   │   │   ├── cloudformation.yaml            # Infrastructure as Code
│   │   │   └── requirements.txt
│   │   │
│   │   └── bedrock-agent-secure/
│   │       ├── README.md                      # Deployment instructions
│   │       ├── agent.py                       # Secure Bedrock agent
│   │       ├── lambda_function.py             # Secure action handler
│   │       ├── guardrails.py                  # Bedrock Guardrails config
│   │       ├── cloudformation.yaml            # Secure infrastructure
│   │       └── requirements.txt
│   │
│   └── 06-hands-on-labs/
│       ├── README.md                          # Labs overview
│       ├── lab-01-exploit-direct.md           # Attack direct injection
│       ├── lab-02-exploit-indirect.md         # Attack indirect injection
│       ├── lab-03-implement-defenses.md       # Implement defenses
│       └── lab-04-build-secure-agent.md       # Capstone: build secure agent
│
└── shared/
    ├── aws_utils.py                           # Bedrock helper functions
    ├── logging_config.py                      # Security logging setup
    └── requirements.txt                       # Common dependencies
```

## Implementation Phases

### Phase 1: Foundation & Documentation
**Goal**: Set up project structure and core documentation

**Deliverables**:
- [ ] Main README.md with course overview
- [ ] Module 01 README.md with theory
- [ ] Comparison documentation (03-why-different-from-code-injection/)
- [ ] Shared utilities structure

**Estimated Time**: 1-2 hours

---

### Phase 2: Direct Injection Examples (EXPANDED)
**Goal**: Demonstrate direct prompt injection attacks and architectural defenses across different models

**Deliverables**:
- [x] Vulnerable chatbot - Claude (01-direct-injection/vulnerable-agent/)
- [x] Vulnerable chatbot - Titan (01-direct-injection/vulnerable-agent-titan/)
- [x] Secure chatbot - Claude (01-direct-injection/secure-agent/)
- [x] Secure chatbot - Titan (01-direct-injection/secure-agent-titan/)
- [x] 6 realistic attack examples
- [x] Automated testing scripts
- [x] Model comparison tools (compare_models.py, compare_all.py)
- [x] Comprehensive documentation (5 additional docs)

**Key Features**:
- 4 agent combinations (Model x Architecture matrix)
- Proves: Architecture > Model Safety
- Vulnerable Claude: ~17% attack success
- Vulnerable Titan: ~50-83% attack success
- Secure Claude: 0% attack success
- Secure Titan: 0% attack success
- Privilege separation, output validation
- Visual comparisons and diagrams

**Actual Time**: ~3 hours (expanded scope)

**Key Insight**: Even weak models (Titan) are secure with proper architecture. Even strong models (Claude) are vulnerable without it.

---

### Phase 3: Indirect Injection Examples
**Goal**: Demonstrate indirect injection through external data sources

**Deliverables**:
- [ ] Agent with document processing (02-indirect-injection/vulnerable-agent/)
- [ ] Poisoned data sources (documents, emails, webpages)
- [ ] Privilege-separated secure agent (02-indirect-injection/secure-agent/)
- [ ] Architecture documentation

**Key Features**:
- RAG-style document retrieval
- Hidden instructions in external content
- Separate reader/executor agents
- Trust boundary enforcement

**Estimated Time**: 3-4 hours

---

### Phase 4: Architecture Defense Patterns
**Goal**: Implement 4 core architectural defense patterns

**Deliverables**:
- [ ] Pattern 1: Privilege Separation (separate agents for different tasks)
- [ ] Pattern 2: Output Validation (structured outputs, schema validation)
- [ ] Pattern 3: Sandboxing (isolated execution environments)
- [ ] Pattern 4: Human-in-the-Loop (approval workflows)

**Key Features**:
- Working code for each pattern
- Architecture diagrams
- Use case explanations

**Estimated Time**: 4-5 hours

---

### Phase 5: AWS Bedrock Integration
**Goal**: Production-ready examples using AWS services

**Deliverables**:
- [ ] Vulnerable Bedrock Agent with action groups
- [ ] Secure Bedrock Agent with Guardrails
- [ ] Lambda functions for action handlers
- [ ] CloudFormation templates
- [ ] IAM policies and security configurations

**Key Features**:
- Bedrock Agents API
- Bedrock Guardrails
- CloudWatch logging
- IAM least privilege
- Secrets Manager integration

**Estimated Time**: 5-6 hours

---

### Phase 6: Hands-on Labs
**Goal**: Student exercises with guided instructions

**Deliverables**:
- [ ] Lab 1: Exploit direct injection (guided attack scenarios)
- [ ] Lab 2: Exploit indirect injection (RAG poisoning)
- [ ] Lab 3: Implement defenses (fix vulnerable code)
- [ ] Lab 4: Build secure agent from scratch (capstone)

**Key Features**:
- Step-by-step instructions
- Success criteria
- Solution guides
- Assessment rubrics

**Estimated Time**: 3-4 hours

---

## Technology Stack

### AWS Services
- **Amazon Bedrock**: Claude 3 Haiku (strong safety), Amazon Titan Text Express (weaker safety)
- **AWS Lambda**: Action group handlers
- **IAM**: Least privilege policies
- **CloudWatch**: Security logging and monitoring
- **Bedrock Guardrails**: Content filtering and safety
- **Secrets Manager**: Credential management
- **CloudFormation**: Infrastructure as Code

### Python Libraries
- **boto3**: AWS SDK
- **pydantic**: Data validation
- **flask/fastapi**: Web frameworks (for demos)
- **pytest**: Testing
- **python-dotenv**: Environment management

### Development Tools
- Python 3.11+
- AWS CLI
- Docker (optional, for sandboxing examples)

## Prerequisites

### For Students
- AWS Account with Bedrock access
- Python 3.11+ installed
- AWS CLI configured
- Basic understanding of:
  - Python programming
  - REST APIs
  - AWS basics (IAM, Lambda)
  - LLM concepts

### For Instructors
- All student prerequisites
- CloudFormation deployment experience
- Understanding of security principles
- Bedrock Agents experience

## Success Metrics

### Knowledge Outcomes
- Students can explain why prompt injection differs from code injection
- Students can identify direct vs indirect injection vectors
- Students understand why detection alone is insufficient
- Students can design architectures with defense-in-depth
- **Students understand architecture matters more than model choice**
- **Students can explain why even weak models can be secured**

### Practical Outcomes
- Students can exploit vulnerable agents (in controlled environment)
- Students can implement privilege separation
- Students can configure Bedrock Guardrails
- Students can build secure agents from scratch

## Security Considerations

### Course Delivery
- All attacks demonstrated in isolated environments
- No real user data or production systems
- Clear ethical guidelines for students
- Responsible disclosure practices

### Example Code
- Clearly labeled "vulnerable" vs "secure"
- Comments explaining security implications
- No real credentials in code
- Sanitized example data

## Future Enhancements
- Multi-agent system security
- Advanced evasion techniques
- Automated security testing
- Integration with CI/CD pipelines
- Additional cloud providers (Azure OpenAI, GCP Vertex AI)

## References & Resources
- OWASP Top 10 for LLM Applications
- AWS Bedrock Security Best Practices
- Academic papers on prompt injection
- Real-world incident case studies
