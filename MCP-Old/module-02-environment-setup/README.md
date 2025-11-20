# Module 2: Environment Setup with Amazon Bedrock

## Learning Objectives
- Set up Python environment for MCP development
- Configure AWS credentials and Bedrock access
- Install and configure MCP libraries
- Test connection to Amazon Bedrock models
- Create your first MCP-Bedrock integration

## Prerequisites
- Python 3.8 or higher
- AWS account with Bedrock access
- Basic command line knowledge

## Step 1: Python Environment Setup

### Create Virtual Environment
```bash
# Create virtual environment
python -m venv mcp-env

# Activate environment (Linux/Mac)
source mcp-env/bin/activate

# Activate environment (Windows)
mcp-env\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: AWS Configuration

### Install AWS CLI
```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure
```

### Required Information
- **Access Key ID**: Your AWS access key
- **Secret Access Key**: Your AWS secret key
- **Default Region**: us-east-1 (recommended for Bedrock)
- **Output Format**: json

### Verify AWS Configuration
```bash
# Test AWS connection
aws sts get-caller-identity

# List available Bedrock models
aws bedrock list-foundation-models --region us-east-1
```

## Step 3: Amazon Bedrock Setup

### Enable Model Access
1. Go to AWS Console → Amazon Bedrock
2. Navigate to "Model access" in the left sidebar
3. Click "Enable specific models"
4. Enable these models:
   - Claude 3.5 Sonnet
   - Claude 3 Haiku
   - Titan Text G1 - Express

### Test Bedrock Access
```python
import boto3

# Create Bedrock client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# Test with Claude 3 Haiku
response = bedrock.invoke_model(
    modelId='anthropic.claude-3-haiku-20240307-v1:0',
    body='{"messages":[{"role":"user","content":"Hello!"}],"max_tokens":100}'
)

print(response)
```

## Step 4: MCP Library Installation

### Core MCP Package
```bash
pip install mcp
```

### Additional Utilities
```bash
pip install mcp-server-stdio
pip install mcp-client
```

## Step 5: Environment Variables

### Create .env File
```bash
# Create environment file
touch .env
```

### Add Configuration
```env
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Bedrock Models
BEDROCK_CLAUDE_SONNET=anthropic.claude-3-5-sonnet-20241022-v2:0
BEDROCK_CLAUDE_HAIKU=anthropic.claude-3-haiku-20240307-v1:0
BEDROCK_TITAN_TEXT=amazon.titan-text-express-v1

# MCP Configuration
MCP_SERVER_PORT=8000
MCP_LOG_LEVEL=INFO
```

## Step 6: Test Your Setup

### Basic MCP Server Test
```python
# test_mcp_server.py
from mcp import Server
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    server = Server("test-server")
    
    @server.tool()
    async def hello(name: str) -> str:
        return f"Hello, {name}!"
    
    print("MCP Server is working!")
    print("Available tools:", [tool.name for tool in server.tools])

if __name__ == "__main__":
    asyncio.run(main())
```

### Bedrock Integration Test
```python
# test_bedrock.py
import boto3
import json
from dotenv import load_dotenv
import os

load_dotenv()

def test_bedrock():
    client = boto3.client(
        'bedrock-runtime',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    
    # Test Claude 3 Haiku
    body = json.dumps({
        "messages": [{"role": "user", "content": "Say hello in 3 languages"}],
        "max_tokens": 100,
        "anthropic_version": "bedrock-2023-05-31"
    })
    
    response = client.invoke_model(
        modelId=os.getenv('BEDROCK_CLAUDE_HAIKU'),
        body=body
    )
    
    result = json.loads(response['body'].read())
    print("Bedrock Response:", result['content'][0]['text'])

if __name__ == "__main__":
    test_bedrock()
```

## Step 7: Project Structure

### Recommended Directory Structure
```
mcp-course/
├── .env
├── requirements.txt
├── servers/
│   ├── __init__.py
│   └── basic_server.py
├── clients/
│   ├── __init__.py
│   └── bedrock_client.py
├── utils/
│   ├── __init__.py
│   ├── bedrock_helper.py
│   └── mcp_helper.py
└── tests/
    ├── test_server.py
    └── test_client.py
```

## Step 8: Troubleshooting

### Common Issues

**1. AWS Credentials Not Found**
```bash
# Check AWS configuration
aws configure list

# Set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

**2. Bedrock Access Denied**
- Ensure model access is enabled in AWS Console
- Check IAM permissions for Bedrock
- Verify region is correct (us-east-1)

**3. MCP Import Errors**
```bash
# Reinstall MCP
pip uninstall mcp
pip install mcp --upgrade
```

**4. Python Version Issues**
```bash
# Check Python version
python --version

# Should be 3.8 or higher
```

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] AWS CLI configured
- [ ] Bedrock models enabled
- [ ] MCP libraries installed
- [ ] Environment variables set
- [ ] Test scripts run successfully

## Next Steps

In Module 3, we'll build your first MCP server with practical tools and integrate it with Amazon Bedrock models.

## Quick Commands Reference

```bash
# Activate environment
source mcp-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test AWS connection
aws sts get-caller-identity

# Run test scripts
python test_mcp_server.py
python test_bedrock.py
```