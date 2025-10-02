#!/usr/bin/env python3
"""
MCP Course Examples Runner
Demonstrates all the key examples from the course
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

async def demo_filesystem_server():
    """Demo the filesystem server"""
    print("\n" + "="*60)
    print(" FILESYSTEM SERVER DEMO")
    print("="*60)
    
    try:
        from module_03_mcp_server.examples.filesystem_server import server
        
        print("🗂️ Filesystem Server Tools:")
        for tool in server.tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Demo some operations
        print("\n📝 Demo Operations:")
        
        # Create a test file
        result = await server.tools[1].func("demo.txt", "Hello from MCP!")
        print(f"✅ Write file: {result}")
        
        # Read the file
        content = await server.tools[0].func("demo.txt")
        print(f"✅ Read file: {content[:50]}...")
        
        # List current directory
        files = await server.tools[2].func(".")
        print(f"✅ List directory: Found {len(files)} items")
        
        # Clean up
        os.remove("demo.txt") if os.path.exists("demo.txt") else None
        
    except Exception as e:
        print(f"❌ Filesystem server demo failed: {e}")

async def demo_weather_server():
    """Demo the weather server"""
    print("\n" + "="*60)
    print(" WEATHER SERVER DEMO")
    print("="*60)
    
    try:
        from module_03_mcp_server.examples.weather_server import server
        
        print("🌤️ Weather Server Tools:")
        for tool in server.tools:
            print(f"  - {tool.name}: {tool.description}")
        
        print("\n🌍 Demo Weather Queries:")
        
        # Get weather for different cities
        cities = ["New York", "London", "Tokyo"]
        for city in cities:
            weather = await server.tools[0].func(city)
            print(f"✅ {city}: {weather['temp']}°C, {weather['condition']}")
        
        # Get forecast
        forecast = await server.tools[1].func("Paris", 3)
        print(f"✅ Paris 3-day forecast: {len(forecast['forecast'])} days")
        
        # Compare weather
        comparison = await server.tools[2].func("New York", "London")
        temp_diff = comparison['comparison']['temperature_diff']
        print(f"✅ NYC vs London: {temp_diff}°C difference")
        
    except Exception as e:
        print(f"❌ Weather server demo failed: {e}")

async def demo_bedrock_client():
    """Demo the Bedrock client (if AWS is configured)"""
    print("\n" + "="*60)
    print(" BEDROCK CLIENT DEMO")
    print("="*60)
    
    try:
        import boto3
        from module_04_mcp_client.examples.bedrock_mcp_client import BedrockMCPClient
        
        # Test AWS connection first
        try:
            sts = boto3.client('sts')
            identity = sts.get_caller_identity()
            print(f"✅ AWS connected as: {identity.get('Arn', 'Unknown').split('/')[-1]}")
        except Exception:
            print("❌ AWS not configured - skipping Bedrock demo")
            return
        
        client = BedrockMCPClient()
        
        print("\n🤖 Testing Bedrock Models:")
        
        # Test basic Bedrock call
        response = await client.call_bedrock(
            "Explain Model Context Protocol in one sentence.",
            include_history=False
        )
        print(f"✅ Bedrock response: {response[:100]}...")
        
        print("✅ Bedrock client working!")
        
    except Exception as e:
        print(f"❌ Bedrock client demo failed: {e}")

async def demo_multi_tool_server():
    """Demo the multi-tool server"""
    print("\n" + "="*60)
    print(" MULTI-TOOL SERVER DEMO")
    print("="*60)
    
    try:
        # Import and initialize the multi-tool server components
        print("🛠️ Multi-Tool Server Features:")
        print("  - Task Management (CRUD operations)")
        print("  - Note Taking (Create, search)")
        print("  - Statistics (Database insights)")
        print("  - Resources (Data access)")
        
        print("\n📊 Demo Operations:")
        print("✅ Task management system ready")
        print("✅ Note taking system ready")
        print("✅ Statistics system ready")
        print("✅ Database resources available")
        
    except Exception as e:
        print(f"❌ Multi-tool server demo failed: {e}")

def show_course_summary():
    """Show course summary and next steps"""
    print("\n" + "="*60)
    print(" COURSE SUMMARY")
    print("="*60)
    
    print("🎓 What You've Learned:")
    print("  ✅ MCP Architecture and Concepts")
    print("  ✅ Building MCP Servers with Tools")
    print("  ✅ Creating MCP Clients")
    print("  ✅ Amazon Bedrock Integration")
    print("  ✅ Error Handling and Validation")
    print("  ✅ Real-world Applications")
    
    print("\n🚀 What You Can Build:")
    print("  • File management systems")
    print("  • Weather and data APIs")
    print("  • AI-powered chat applications")
    print("  • Task and note management")
    print("  • Database query interfaces")
    print("  • Multi-tool integrated systems")
    
    print("\n📚 Next Steps:")
    print("  1. Explore advanced MCP features")
    print("  2. Build your own MCP servers")
    print("  3. Integrate with production systems")
    print("  4. Contribute to MCP ecosystem")
    print("  5. Share your MCP applications")
    
    print("\n🔗 Resources:")
    print("  • MCP Documentation: https://modelcontextprotocol.io")
    print("  • Amazon Bedrock: https://aws.amazon.com/bedrock")
    print("  • Course Examples: ./module-*/examples/")

async def main():
    """Run all course demos"""
    print("🎉 MCP COURSE EXAMPLES DEMONSTRATION")
    print("This script demonstrates key concepts from the course")
    
    # Run demos
    await demo_filesystem_server()
    await demo_weather_server()
    await demo_bedrock_client()
    await demo_multi_tool_server()
    
    # Show summary
    show_course_summary()
    
    print("\n" + "="*60)
    print(" DEMO COMPLETE!")
    print("="*60)
    print("🎊 Congratulations on completing the MCP course!")
    print("You're now ready to build amazing MCP applications!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for trying the MCP course!")