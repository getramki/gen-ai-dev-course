# Module 2: Setup and Environment (10 minutes)

## Learning Objectives
- Configure Python environment for LangChain-AWS integration
- Set up AWS Bedrock access and permissions
- Establish secure credential management
- Test LangChain-AWS connectivity

## Prerequisites
- AWS Account with Bedrock access
- Python 3.8+ installed
- AWS CLI installed
- Module 1 completed

## Module Structure
1. **Topic 2.1**: Environment Setup and Dependencies (3 min)
2. **Topic 2.2**: AWS Bedrock Configuration and Model Access (4 min)
3. **Topic 2.3**: LangChain-AWS Integration Setup (3 min)

## Setup Instructions
```bash
# Navigate to module2
cd module2

# Install AWS-specific dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure
```

## Files in this Module
- `topic_2_1_environment.py` - Environment setup and dependency verification
- `topic_2_2_bedrock_config.py` - AWS Bedrock configuration and testing
- `topic_2_3_integration.py` - LangChain-AWS integration setup
- `requirements.txt` - Module-specific dependencies
- `exercises/` - Hands-on practice files

## Quick Start
Run each topic file to verify setup:
```bash
python topic_2_1_environment.py
python topic_2_2_bedrock_config.py
python topic_2_3_integration.py
```

## Important Notes
- Ensure AWS credentials are configured before starting
- Some Bedrock models require access requests
- Keep credentials secure and never commit them to code
- Test connectivity before proceeding to Module 3