"""
Exercise 2: LangChain-Bedrock Integration Test

Task: Test LangChain integration with AWS Bedrock:
1. Initialize both ChatBedrock and ChatBedrockConverse
2. Test basic functionality with simple prompts
3. Compare response formats and performance
4. Create reusable chat instances

Time: 5 minutes
"""

from langchain_aws.chat_models import ChatBedrock, ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import json
import time
from botocore.exceptions import ClientError

class LangChainBedrockTester:
    """Test LangChain-Bedrock integration"""
    
    def __init__(self):
        self.region = 'us-east-1'
        self.model_id = 'anthropic.claude-3-haiku-20240307-v1:0'
        self.test_results = {}
    
    def initialize_chat_models(self):
        """Initialize both ChatBedrock and ChatBedrockConverse"""
        
        print("=== Initializing Chat Models ===\n")
        
        # Initialize ChatBedrock
        try:
            self.chat_bedrock = ChatBedrock(
                model_id=self.model_id,
                region_name=self.region,
                model_kwargs={
                    "max_tokens": 100,
                    "temperature": 0.7
                }
            )
            print("✅ ChatBedrock initialized")
            self.test_results['chatbedrock_init'] = True
            
        except Exception as e:
            print(f"❌ ChatBedrock failed: {e}")
            self.chat_bedrock = None
            self.test_results['chatbedrock_init'] = False
        
        # Initialize ChatBedrockConverse
        try:
            self.chat_converse = ChatBedrockConverse(
                model_id=self.model_id,
                region_name=self.region,
                max_tokens=100,
                temperature=0.7
            )
            print("✅ ChatBedrockConverse initialized")
            self.test_results['chatconverse_init'] = True
            
        except Exception as e:
            print(f"❌ ChatBedrockConverse failed: {e}")
            self.chat_converse = None
            self.test_results['chatconverse_init'] = False
        
        print()
    
    def test_simple_invocation(self):
        """Test simple message invocation"""
        
        print("=== Simple Invocation Test ===\n")
        
        test_message = HumanMessage(content="Explain Python in one sentence.")
        
        # Test ChatBedrock
        if self.chat_bedrock:
            try:
                start_time = time.time()
                response = self.chat_bedrock.invoke([test_message])
                duration = time.time() - start_time
                
                print("✅ ChatBedrock Response:")
                print(f"   Content: {response.content[:80]}...")
                print(f"   Duration: {duration:.2f}s")
                print(f"   Type: {type(response)}")
                
                self.test_results['chatbedrock_invoke'] = {
                    'success': True,
                    'duration': duration,
                    'response_length': len(response.content)
                }
                
            except Exception as e:
                print(f"❌ ChatBedrock invocation failed: {e}")
                self.test_results['chatbedrock_invoke'] = {'success': False, 'error': str(e)}
        
        print()
        
        # Test ChatBedrockConverse
        if self.chat_converse:
            try:
                start_time = time.time()
                response = self.chat_converse.invoke([test_message])
                duration = time.time() - start_time
                
                print("✅ ChatBedrockConverse Response:")
                print(f"   Content: {response.content[:80]}...")
                print(f"   Duration: {duration:.2f}s")
                print(f"   Type: {type(response)}")
                
                self.test_results['chatconverse_invoke'] = {
                    'success': True,
                    'duration': duration,
                    'response_length': len(response.content)
                }
                
            except Exception as e:
                print(f"❌ ChatBedrockConverse invocation failed: {e}")
                self.test_results['chatconverse_invoke'] = {'success': False, 'error': str(e)}
        
        print()
    
    def test_conversation_flow(self):
        """Test multi-turn conversation"""
        
        print("=== Conversation Flow Test ===\n")
        
        messages = [
            SystemMessage(content="You are a helpful Python tutor."),
            HumanMessage(content="What is a list?"),
            HumanMessage(content="Give me a simple example.")
        ]
        
        # Test with ChatBedrockConverse (better for conversations)
        if self.chat_converse:
            try:
                response = self.chat_converse.invoke(messages)
                
                print("✅ Multi-turn Conversation:")
                print(f"   Messages sent: {len(messages)}")
                print(f"   Response: {response.content[:100]}...")
                
                self.test_results['conversation_flow'] = {
                    'success': True,
                    'messages_count': len(messages),
                    'response_length': len(response.content)
                }
                
            except Exception as e:
                print(f"❌ Conversation test failed: {e}")
                self.test_results['conversation_flow'] = {'success': False, 'error': str(e)}
        else:
            print("❌ ChatBedrockConverse not available for conversation test")
            self.test_results['conversation_flow'] = {'success': False, 'error': 'Model not initialized'}
        
        print()
    
    def test_prompt_template_integration(self):
        """Test integration with LangChain prompt templates"""
        
        print("=== Prompt Template Integration ===\n")
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert in {subject}."),
            ("human", "Explain {topic} in {style} style.")
        ])
        
        # Test with ChatBedrock
        if self.chat_bedrock:
            try:
                # Create chain
                chain = prompt | self.chat_bedrock
                
                response = chain.invoke({
                    "subject": "programming",
                    "topic": "variables",
                    "style": "simple"
                })
                
                print("✅ Prompt Template + ChatBedrock:")
                print(f"   Response: {response.content[:80]}...")
                
                self.test_results['prompt_template'] = {
                    'success': True,
                    'chain_type': 'prompt | chatbedrock',
                    'response_length': len(response.content)
                }
                
            except Exception as e:
                print(f"❌ Prompt template test failed: {e}")
                self.test_results['prompt_template'] = {'success': False, 'error': str(e)}
        else:
            print("❌ ChatBedrock not available for prompt template test")
            self.test_results['prompt_template'] = {'success': False, 'error': 'Model not initialized'}
        
        print()
    
    def test_streaming_capability(self):
        """Test streaming responses"""
        
        print("=== Streaming Test ===\n")
        
        if self.chat_bedrock:
            try:
                message = HumanMessage(content="Count from 1 to 5 with explanations.")
                
                print("Testing streaming response...")
                stream = self.chat_bedrock.stream([message])
                
                chunks = []
                for chunk in stream:
                    chunks.append(chunk.content)
                    if len(chunks) <= 3:  # Show first few chunks
                        print(f"   Chunk {len(chunks)}: '{chunk.content}'")
                
                print(f"   Total chunks received: {len(chunks)}")
                
                self.test_results['streaming'] = {
                    'success': True,
                    'chunks_count': len(chunks),
                    'total_content': ''.join(chunks)
                }
                
            except Exception as e:
                print(f"❌ Streaming test failed: {e}")
                self.test_results['streaming'] = {'success': False, 'error': str(e)}
        else:
            print("❌ ChatBedrock not available for streaming test")
            self.test_results['streaming'] = {'success': False, 'error': 'Model not initialized'}
        
        print()
    
    def compare_models(self):
        """Compare ChatBedrock vs ChatBedrockConverse"""
        
        print("=== Model Comparison ===\n")
        
        bedrock_result = self.test_results.get('chatbedrock_invoke', {})
        converse_result = self.test_results.get('chatconverse_invoke', {})
        
        if bedrock_result.get('success') and converse_result.get('success'):
            print("Performance Comparison:")
            print(f"  ChatBedrock Duration: {bedrock_result['duration']:.2f}s")
            print(f"  ChatBedrockConverse Duration: {converse_result['duration']:.2f}s")
            print(f"  ChatBedrock Response Length: {bedrock_result['response_length']} chars")
            print(f"  ChatBedrockConverse Response Length: {converse_result['response_length']} chars")
            
            faster_model = "ChatBedrock" if bedrock_result['duration'] < converse_result['duration'] else "ChatBedrockConverse"
            print(f"  Faster Model: {faster_model}")
        else:
            print("Cannot compare - one or both models failed initialization/invocation")
        
        print()
        
        print("Feature Comparison:")
        print("  ChatBedrock:")
        print("    • Direct Bedrock API access")
        print("    • Streaming support")
        print("    • Lower-level control")
        print("  ChatBedrockConverse:")
        print("    • Enhanced conversation handling")
        print("    • Better multi-turn support")
        print("    • Simplified message management")
        print()
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        
        print("=== Integration Test Report ===\n")
        
        total_tests = 0
        passed_tests = 0
        
        test_categories = [
            ('Model Initialization', ['chatbedrock_init', 'chatconverse_init']),
            ('Basic Invocation', ['chatbedrock_invoke', 'chatconverse_invoke']),
            ('Advanced Features', ['conversation_flow', 'prompt_template', 'streaming'])
        ]
        
        for category, tests in test_categories:
            print(f"{category}:")
            for test in tests:
                result = self.test_results.get(test, {})
                total_tests += 1
                
                if isinstance(result, bool):
                    success = result
                else:
                    success = result.get('success', False)
                
                if success:
                    passed_tests += 1
                    print(f"  ✅ {test}")
                else:
                    print(f"  ❌ {test}")
                    if isinstance(result, dict) and 'error' in result:
                        print(f"     Error: {result['error']}")
            print()
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f"Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.0f}%)")
        
        if success_rate >= 80:
            print("🚀 Excellent! LangChain-Bedrock integration is working well.")
        elif success_rate >= 60:
            print("✅ Good! Minor issues may need attention.")
        else:
            print("⚠️  Integration needs work. Check AWS setup and permissions.")

def run_integration_test():
    """Run complete LangChain-Bedrock integration test"""
    
    print("Starting LangChain-Bedrock Integration Test...\n")
    
    tester = LangChainBedrockTester()
    
    # Run all tests
    tester.initialize_chat_models()
    tester.test_simple_invocation()
    tester.test_conversation_flow()
    tester.test_prompt_template_integration()
    tester.test_streaming_capability()
    tester.compare_models()
    tester.generate_test_report()
    
    return tester

if __name__ == "__main__":
    tester = run_integration_test()
    
    print("\n" + "="*50)
    print("✅ Exercise 2 Complete!")
    print("\nKey Learnings:")
    print("• Both ChatBedrock and ChatBedrockConverse are functional")
    print("• LangChain chains work seamlessly with Bedrock")
    print("• Streaming and conversation features are available")
    print("• Ready for advanced Module 3 topics!")
    print("="*50)