#!/usr/bin/env python3
import asyncio
import json
import boto3
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class EMIAgent:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
    async def call_claude(self, prompt):
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps(body)
        )
        
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
    
    async def run(self):
        server_params = StdioServerParameters(
            command="python",
            args=["../2-hl-emi-calc-server/server.py"]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("AI-Powered Home Loan EMI Assistant")
                print("=" * 40)
                print("Ask me anything about home loan EMI calculations!")
                print("Type 'quit' to exit\n")
                
                while True:
                    user_input = input("You: ").strip()
                    if user_input.lower() == 'quit':
                        break
                    
                    prompt = f"""You are an AI assistant that helps with home loan EMI calculations. 
You have access to a tool called 'calculate_home_loan_emi' that takes principal (loan amount), annual_rate (interest rate %), and tenure_years (loan duration in years).

User query: {user_input}

If the user is asking about EMI calculation and provides the necessary details (loan amount, interest rate, tenure), extract these values and respond with: "CALCULATE: principal=X, annual_rate=Y, tenure_years=Z"

If the user needs help or clarification, provide helpful guidance about home loan EMI calculations.

If the query is not related to EMI calculations, politely redirect to EMI-related topics."""

                    try:
                        print(f"DEBUG: Sending prompt to Bedrock...")
                        ai_response = await self.call_claude(prompt)
                        print(f"DEBUG: Bedrock response: {ai_response}")
                        
                        if ai_response.startswith("CALCULATE:"):
                            print(f"DEBUG: Detected calculation request")
                            # Extract parameters
                            params_str = ai_response.replace("CALCULATE:", "").strip()
                            print(f"DEBUG: Extracted params string: {params_str}")
                            extracted = {}
                            for param in params_str.split(", "):
                                key, value = param.split("=")
                                if key == "tenure_years":
                                    extracted[key] = int(value)
                                else:
                                    extracted[key] = float(value)
                            
                            # Format parameters correctly
                            params = {
                                "principal": extracted["principal"],
                                "annual_rate": extracted["annual_rate"],
                                "tenure_years": extracted["tenure_years"]
                            }
                            print(f"DEBUG: Formatted params: {params}")
                            
                            # Call MCP tool
                            print(f"DEBUG: Calling MCP tool...")
                            result = await session.call_tool("calculate_home_loan_emi", params)
                            print(f"DEBUG: MCP tool result: {result.content[0].text}")
                            print(f"Assistant: {result.content[0].text}")
                        else:
                            print(f"DEBUG: Providing general response")
                            print(f"Assistant: {ai_response}")
                            
                    except Exception as e:
                        print(f"Assistant: Sorry, I encountered an error: {e}")

async def main():
    agent = EMIAgent()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())