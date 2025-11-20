#!/usr/bin/env python3
"""
MCP Course Setup Script
Helps students set up their environment and verify everything is working
"""

import os
import sys
import subprocess
import asyncio
import json
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n{step}. {description}")
    print("-" * 40)

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False

def check_pip_packages():
    """Check if required packages are installed"""
    required_packages = [
        'boto3', 'mcp', 'python-dotenv', 'asyncio-mqtt', 
        'pydantic', 'httpx', 'websockets', 'pytest'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    return missing_packages

def install_packages(packages):
    """Install missing packages"""
    if not packages:
        return True
    
    print(f"\nInstalling missing packages: {', '.join(packages)}")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install'
        ] + packages)
        print("✅ Packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
        return False

def check_aws_credentials():
    """Check AWS credentials"""
    try:
        import boto3
        
        # Try to create a client and get caller identity
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print(f"✅ AWS credentials configured")
        print(f"   Account: {identity.get('Account', 'Unknown')}")
        print(f"   User: {identity.get('Arn', 'Unknown').split('/')[-1]}")
        return True
        
    except Exception as e:
        print(f"❌ AWS credentials not configured: {str(e)}")
        print("   Run: aws configure")
        return False

def check_bedrock_access():
    """Check Amazon Bedrock access"""
    try:
        import boto3
        
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        models = bedrock.list_foundation_models()
        
        print(f"✅ Bedrock access confirmed")
        print(f"   Available models: {len(models['modelSummaries'])}")
        return True
        
    except Exception as e:
        print(f"❌ Bedrock access failed: {str(e)}")
        print("   Enable model access in AWS Console")
        return False

async def test_mcp_basic():
    """Test basic MCP functionality"""
    try:
        from mcp import Server
        
        server = Server("test-server")
        
        @server.tool()
        async def test_tool(message: str) -> str:
            return f"Echo: {message}"
        
        # Test tool execution
        result = await test_tool("Hello MCP!")
        
        if result == "Echo: Hello MCP!":
            print("✅ MCP basic functionality working")
            return True
        else:
            print("❌ MCP test failed")
            return False
            
    except Exception as e:
        print(f"❌ MCP test error: {str(e)}")
        return False

async def test_bedrock_integration():
    """Test Bedrock integration"""
    try:
        import boto3
        
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        body = json.dumps({
            "messages": [{"role": "user", "content": "Say 'MCP Setup Test Successful'"}],
            "max_tokens": 50,
            "anthropic_version": "bedrock-2023-05-31"
        })
        
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=body
        )
        
        result = json.loads(response['body'].read())
        response_text = result['content'][0]['text']
        
        if "MCP Setup Test Successful" in response_text:
            print("✅ Bedrock integration working")
            print(f"   Response: {response_text}")
            return True
        else:
            print("❌ Bedrock integration test failed")
            return False
            
    except Exception as e:
        print(f"❌ Bedrock integration error: {str(e)}")
        return False

def create_env_file():
    """Create .env file from template"""
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        try:
            content = env_example.read_text()
            env_file.write_text(content)
            print("✅ Created .env file from template")
            print("   Please edit .env with your AWS credentials")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ .env.example not found")
        return False

def show_next_steps():
    """Show next steps for the student"""
    print_header("NEXT STEPS")
    
    print("1. Edit the .env file with your AWS credentials:")
    print("   - AWS_ACCESS_KEY_ID")
    print("   - AWS_SECRET_ACCESS_KEY")
    print("   - AWS_REGION (default: us-east-1)")
    
    print("\n2. Enable Bedrock model access in AWS Console:")
    print("   - Go to Amazon Bedrock → Model access")
    print("   - Enable Claude 3.5 Sonnet and Claude 3 Haiku")
    
    print("\n3. Start with Module 1:")
    print("   cd module-01-mcp-fundamentals")
    print("   Read README.md and complete exercises.md")
    
    print("\n4. Run example servers:")
    print("   python module-03-mcp-server/examples/filesystem_server.py")
    print("   python module-03-mcp-server/examples/weather_server.py")
    
    print("\n5. Test the Bedrock client:")
    print("   python module-04-mcp-client/examples/bedrock_mcp_client.py")

async def main():
    """Main setup function"""
    print_header("MCP COURSE SETUP")
    print("Welcome to the Model Context Protocol hands-on course!")
    print("This script will help you set up your development environment.")
    
    # Step 1: Check Python version
    print_step(1, "Checking Python Version")
    if not check_python_version():
        print("\nPlease install Python 3.8 or higher and try again.")
        return
    
    # Step 2: Check and install packages
    print_step(2, "Checking Required Packages")
    missing = check_pip_packages()
    
    if missing:
        install_choice = input(f"\nInstall missing packages? (y/n): ").lower()
        if install_choice == 'y':
            if not install_packages(missing):
                print("Package installation failed. Please install manually.")
                return
        else:
            print("Please install missing packages manually:")
            print(f"pip install {' '.join(missing)}")
            return
    
    # Step 3: Create .env file
    print_step(3, "Setting up Environment File")
    create_env_file()
    
    # Step 4: Check AWS credentials
    print_step(4, "Checking AWS Configuration")
    aws_ok = check_aws_credentials()
    
    # Step 5: Check Bedrock access
    print_step(5, "Checking Bedrock Access")
    bedrock_ok = check_bedrock_access()
    
    # Step 6: Test MCP functionality
    print_step(6, "Testing MCP Functionality")
    mcp_ok = await test_mcp_basic()
    
    # Step 7: Test Bedrock integration (only if AWS is configured)
    if aws_ok and bedrock_ok:
        print_step(7, "Testing Bedrock Integration")
        bedrock_integration_ok = await test_bedrock_integration()
    else:
        bedrock_integration_ok = False
    
    # Summary
    print_header("SETUP SUMMARY")
    
    checks = [
        ("Python 3.8+", True),
        ("Required packages", len(missing) == 0),
        ("Environment file", True),
        ("AWS credentials", aws_ok),
        ("Bedrock access", bedrock_ok),
        ("MCP functionality", mcp_ok),
        ("Bedrock integration", bedrock_integration_ok)
    ]
    
    all_good = True
    for check_name, status in checks:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check_name}")
        if not status:
            all_good = False
    
    if all_good:
        print("\n🎉 Setup complete! You're ready to start the course.")
    else:
        print("\n⚠️ Some issues need to be resolved before starting.")
    
    show_next_steps()

if __name__ == "__main__":
    asyncio.run(main())