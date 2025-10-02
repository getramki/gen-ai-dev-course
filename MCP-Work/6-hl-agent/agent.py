#!/usr/bin/env python3
import asyncio
import json
import boto3
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class HomeLoanAgent:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.resources = {}
        self.prompts = {}
        
    async def call_claude(self, prompt):
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps(body)
        )
        
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
    
    async def load_resources_and_tools(self, session):
        """Load all resources and advisory tools from MCP server"""
        try:
            # Load resources
            resources = await session.list_resources()
            for resource in resources.resources:
                content = await session.read_resource(resource.uri)
                self.resources[resource.name] = content.contents[0].text
                print(f"DEBUG: Loaded resource '{resource.name}'")
            
            # Load advisory tools
            advice_result = await session.call_tool("get_emi_advice", {})
            self.prompts['emi-advisor'] = advice_result.content[0].text
            print(f"DEBUG: Loaded EMI advice")
            
            comparison_result = await session.call_tool("get_loan_comparison_guide", {})
            self.prompts['loan-comparison'] = comparison_result.content[0].text
            print(f"DEBUG: Loaded loan comparison guide")
                
        except Exception as e:
            print(f"DEBUG: Error loading resources/tools: {e}")
    
    async def run(self):
        server_params = StdioServerParameters(
            command="python",
            args=["../5-hl-emi-calc-server-resource-prompts/server.py"]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                await self.load_resources_and_tools(session)
                
                print("🏠 Home Loan Advisory Agent")
                print("=" * 40)
                print("I can help with EMI calculations, loan advice, and comparisons!")
                print("Type 'quit' to exit\n")
                
                while True:
                    user_input = input("You: ").strip()
                    if user_input.lower() == 'quit':
                        break
                    
                    # Build context with resources and prompts
                    context = f"""You are a home loan advisor with access to the following information:

RESOURCES:
{self.resources.get('emi-formula', '')}

{self.resources.get('interest-rates', '')}

{self.resources.get('loan-eligibility', '')}

ADVISORY GUIDELINES:
{self.prompts.get('emi-advisor', '')}

User query: {user_input}

If the user needs EMI calculation with specific values, respond with: "CALCULATE: principal=X, annual_rate=Y, tenure_years=Z"

Otherwise, provide helpful advice using the available resources."""

                    try:
                        print(f"DEBUG: Sending enhanced prompt to Bedrock...")
                        ai_response = await self.call_claude(context)
                        print(f"DEBUG: Bedrock response: {ai_response}")
                        
                        if ai_response.startswith("CALCULATE:"):
                            print(f"DEBUG: Detected calculation request")
                            params_str = ai_response.replace("CALCULATE:", "").strip()
                            print(f"DEBUG: Extracted params string: {params_str}")
                            
                            extracted = {}
                            for param in params_str.split(", "):
                                key, value = param.split("=")
                                if key == "tenure_years":
                                    extracted[key] = int(value)
                                else:
                                    extracted[key] = float(value)
                            
                            params = {
                                "principal": extracted["principal"],
                                "annual_rate": extracted["annual_rate"],
                                "tenure_years": extracted["tenure_years"]
                            }
                            print(f"DEBUG: Formatted params: {params}")
                            
                            print(f"DEBUG: Calling MCP tool...")
                            result = await session.call_tool("calculate_home_loan_emi", params)
                            print(f"Assistant: {result.content[0].text}")
                        else:
                            print(f"Assistant: {ai_response}")
                            
                    except Exception as e:
                        print(f"Assistant: Sorry, I encountered an error: {e}")

async def main():
    agent = HomeLoanAgent()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())