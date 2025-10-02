"""
Topic 2.1: Environment Setup and Dependencies (3 minutes)

Learning Goals:
- Verify Python environment and dependencies
- Set up virtual environment best practices
- Validate LangChain and AWS package installations
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check Python version compatibility"""
    
    print("=== Python Environment Check ===\n")
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
    else:
        print("❌ Python 3.8+ required")
        return False
    
    print(f"Python Executable: {sys.executable}\n")
    return True

def check_required_packages():
    """Check if required packages are installed"""
    
    print("=== Package Installation Check ===\n")
    
    required_packages = [
        ("langchain", "LangChain core framework"),
        ("langchain_aws", "LangChain AWS integration"),
        ("boto3", "AWS SDK for Python"),
        ("dotenv", "Environment variable management")
    ]
    
    all_installed = True
    
    for package, description in required_packages:
        try:
            if package == "dotenv":
                import_name = "dotenv"
            else:
                import_name = package
            
            spec = importlib.util.find_spec(import_name)
            if spec is not None:
                print(f"✅ {package} - {description}")
            else:
                print(f"❌ {package} - {description} (NOT INSTALLED)")
                all_installed = False
        except ImportError:
            print(f"❌ {package} - {description} (NOT INSTALLED)")
            all_installed = False
    
    print()
    return all_installed

def check_virtual_environment():
    """Check if running in virtual environment"""
    
    print("=== Virtual Environment Check ===\n")
    
    in_venv = (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    if in_venv:
        print("✅ Running in virtual environment")
        print(f"Virtual Environment Path: {sys.prefix}")
    else:
        print("⚠️  Not running in virtual environment")
        print("Recommendation: Use virtual environment for isolation")
    
    print()
    return in_venv

def install_missing_packages():
    """Provide installation commands for missing packages"""
    
    print("=== Installation Commands ===\n")
    
    print("If packages are missing, run:")
    print("pip install langchain langchain-aws boto3 python-dotenv")
    print()
    
    print("For virtual environment setup:")
    print("python -m venv langchain-env")
    print("source langchain-env/bin/activate  # On Windows: langchain-env\\Scripts\\activate")
    print("pip install -r requirements.txt")
    print()

def verify_imports():
    """Test importing key modules"""
    
    print("=== Import Verification ===\n")
    
    imports_to_test = [
        ("from langchain_core.runnables import Runnable", "LangChain Core"),
        ("from langchain_aws.chat_models import ChatBedrock", "LangChain AWS ChatBedrock"),
        ("import boto3", "AWS SDK"),
        ("from dotenv import load_dotenv", "Environment Variables")
    ]
    
    for import_statement, description in imports_to_test:
        try:
            exec(import_statement)
            print(f"✅ {description}")
        except ImportError as e:
            print(f"❌ {description} - {str(e)}")
        except Exception as e:
            print(f"⚠️  {description} - {str(e)}")
    
    print()

def create_env_template():
    """Create .env template file"""
    
    print("=== Environment Template ===\n")
    
    env_template = """# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=us-east-1

# Optional: AWS Profile
AWS_PROFILE=default

# Bedrock Configuration
BEDROCK_REGION=us-east-1
"""
    
    try:
        with open('.env.template', 'w') as f:
            f.write(env_template)
        print("✅ Created .env.template file")
        print("Copy to .env and add your AWS credentials")
    except Exception as e:
        print(f"❌ Could not create .env.template: {e}")
    
    print()

if __name__ == "__main__":
    print("Module 2.1: Environment Setup and Dependencies\n")
    
    # Run all checks
    python_ok = check_python_version()
    packages_ok = check_required_packages()
    venv_status = check_virtual_environment()
    
    verify_imports()
    create_env_template()
    install_missing_packages()
    
    # Summary
    print("="*50)
    print("✅ Topic 2.1 Complete!")
    print("Environment Status:")
    print(f"• Python Version: {'✅' if python_ok else '❌'}")
    print(f"• Required Packages: {'✅' if packages_ok else '❌'}")
    print(f"• Virtual Environment: {'✅' if venv_status else '⚠️'}")
    
    if python_ok and packages_ok:
        print("\n🚀 Ready for AWS Bedrock configuration!")
    else:
        print("\n⚠️  Please install missing dependencies before continuing")
    
    print("="*50)