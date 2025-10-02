#!/usr/bin/env python3
import asyncio
import subprocess
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["../2-hl-emi-calc-server/server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Home Loan EMI Calculator Client")
            print("-" * 32)
            
            try:
                principal = float(input("Enter loan amount: "))
                annual_rate = float(input("Enter annual interest rate (%): "))
                tenure_years = int(input("Enter loan tenure (years): "))
                
                result = await session.call_tool(
                    "calculate_home_loan_emi",
                    {
                        "principal": principal,
                        "annual_rate": annual_rate,
                        "tenure_years": tenure_years
                    }
                )
                
                print("\n" + result.content[0].text)
                
            except ValueError:
                print("Please enter valid numbers")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())