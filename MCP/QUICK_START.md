# MCP Course Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Setup Environment
```bash
# Clone or navigate to the course directory
cd /home/ramakrishna/Code/GenAI-for-Dev-Course/MCP

# Run setup script
python setup_course.py
```

### Step 2: Configure AWS
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your AWS credentials
# AWS_ACCESS_KEY_ID=your_key
# AWS_SECRET_ACCESS_KEY=your_secret
```

### Step 3: Test Your Setup
```bash
# Test basic MCP functionality
python module-02-environment-setup/examples/test_mcp_basic.py

# Test Bedrock connection
python module-02-environment-setup/examples/test_bedrock.py
```

### Step 4: Run Your First MCP Server
```bash
# Start the filesystem server
python module-03-mcp-server/examples/filesystem_server.py
```

### Step 5: Try the Bedrock Client
```bash
# In another terminal, run the client
python module-04-mcp-client/examples/bedrock_mcp_client.py
```

## 📚 Course Structure

| Module | Topic | Time | Key Learning |
|--------|-------|------|--------------|
| 1 | MCP Fundamentals | 30min | Architecture, concepts |
| 2 | Environment Setup | 45min | AWS, Bedrock, MCP setup |
| 3 | Building MCP Server | 45min | Create tools, handle errors |
| 4 | Creating MCP Client | 30min | Bedrock integration |
| 5 | Tools & Resources | 45min | Advanced features |
| 6 | Prompts & Templates | 45min | Reusable AI interactions |
| 7 | Advanced Features | 30min | Complex scenarios |
| 8 | Real-world Apps | 45min | Production examples |
| 9 | Testing & Debugging | 30min | Quality assurance |
| 10 | Deployment | 15min | Best practices |

## 🎯 Learning Path

### Beginner (Day 1)
1. Read Module 1 README
2. Complete Module 1 exercises
3. Set up environment (Module 2)
4. Build first server (Module 3)

### Intermediate (Day 2)
1. Create MCP client (Module 4)
2. Explore tools & resources (Module 5)
3. Work with prompts (Module 6)

### Advanced (Day 3)
1. Advanced features (Module 7)
2. Build real-world app (Module 8)
3. Testing & deployment (Modules 9-10)

## 🛠️ What You'll Build

### Day 1 Projects
- **Filesystem Server**: File operations via MCP
- **Weather Server**: Mock weather API
- **Basic Client**: Connect to servers

### Day 2 Projects
- **Task Manager**: Full CRUD operations
- **Note Taking**: Search and organize
- **Bedrock Chat**: AI-powered interactions

### Day 3 Projects
- **Multi-Server Client**: Connect to multiple servers
- **Production App**: Scalable MCP application
- **Testing Suite**: Comprehensive tests

## 🔧 Tools You'll Use

- **Python 3.8+**: Core programming language
- **MCP Library**: Model Context Protocol implementation
- **Amazon Bedrock**: AI models (Claude, Titan)
- **SQLite**: Local database for examples
- **Pytest**: Testing framework

## 📖 Key Concepts

### MCP Architecture
```
Client ←→ Protocol ←→ Server
  ↓         ↓         ↓
Bedrock   JSON-RPC   Tools
Models    Messages   Resources
                     Prompts
```

### Core Components
- **Tools**: Executable functions
- **Resources**: Data providers
- **Prompts**: Template interactions
- **Clients**: AI applications
- **Servers**: Service providers

## 🎓 Learning Outcomes

After completing this course, you'll be able to:

✅ **Understand MCP**: Architecture and core concepts  
✅ **Build Servers**: Create MCP servers with tools and resources  
✅ **Create Clients**: Integrate with Amazon Bedrock models  
✅ **Handle Data**: Work with different data types and formats  
✅ **Error Management**: Implement robust error handling  
✅ **Security**: Apply security best practices  
✅ **Testing**: Write comprehensive tests  
✅ **Deployment**: Deploy MCP applications  

## 🆘 Getting Help

### Common Issues
1. **AWS Credentials**: Run `aws configure`
2. **Python Version**: Need 3.8+
3. **Package Issues**: Run `pip install -r requirements.txt`
4. **Bedrock Access**: Enable models in AWS Console

### Resources
- Module README files for detailed explanations
- Example code in each module's `examples/` folder
- Solutions in `solutions/` folders
- AWS Bedrock documentation

### Support Checklist
- [ ] Python 3.8+ installed
- [ ] AWS credentials configured
- [ ] Bedrock models enabled
- [ ] Required packages installed
- [ ] .env file configured

## 🚀 Ready to Start?

1. **Run setup**: `python setup_course.py`
2. **Start Module 1**: `cd module-01-mcp-fundamentals`
3. **Read README**: Understanding the concepts
4. **Do exercises**: Hands-on practice
5. **Build projects**: Apply your learning

**Happy learning! 🎉**