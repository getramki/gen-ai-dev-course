#!/usr/bin/env python3
"""
Secure Bedrock Application with Content Filtering
This application demonstrates how to integrate Bedrock Guardrails with a chat application.
"""

import boto3
import json
import streamlit as st
from datetime import datetime
from botocore.exceptions import ClientError

class SecureBedrockApp:
    def __init__(self, guardrail_id, guardrail_version='DRAFT', region='us-east-1'):
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        self.bedrock = boto3.client('bedrock', region_name=region)
        self.guardrail_id = guardrail_id
        self.guardrail_version = guardrail_version
        self.model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    
    def apply_input_guardrail(self, user_input):
        """Apply guardrail to user input"""
        try:
            response = self.bedrock.apply_guardrail(
                guardrailIdentifier=self.guardrail_id,
                guardrailVersion=self.guardrail_version,
                source='INPUT',
                content=[
                    {
                        'text': {
                            'text': user_input
                        }
                    }
                ]
            )
            
            action = response['action']
            
            if action == 'GUARDRAIL_INTERVENED':
                # Log the intervention
                self._log_guardrail_intervention('INPUT', user_input, response)
                return False, "Your message contains content that violates our content policy. Please rephrase your request."
            
            return True, user_input
            
        except ClientError as e:
            st.error(f"Error applying input guardrail: {e}")
            return False, "Error processing your request."
    
    def apply_output_guardrail(self, model_output):
        """Apply guardrail to model output"""
        try:
            response = self.bedrock.apply_guardrail(
                guardrailIdentifier=self.guardrail_id,
                guardrailVersion=self.guardrail_version,
                source='OUTPUT',
                content=[
                    {
                        'text': {
                            'text': model_output
                        }
                    }
                ]
            )
            
            action = response['action']
            
            if action == 'GUARDRAIL_INTERVENED':
                # Log the intervention
                self._log_guardrail_intervention('OUTPUT', model_output, response)
                return False, "I apologize, but I cannot provide that response due to content policy restrictions."
            
            return True, model_output
            
        except ClientError as e:
            st.error(f"Error applying output guardrail: {e}")
            return False, "Error processing the response."
    
    def _log_guardrail_intervention(self, source, content, response):
        """Log guardrail interventions for monitoring"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'action': response['action'],
            'content_length': len(content),
            'guardrail_id': self.guardrail_id,
            'assessments': response.get('assessments', [])
        }
        
        # In production, send this to CloudWatch Logs
        print(f"GUARDRAIL_INTERVENTION: {json.dumps(log_entry)}")
    
    def invoke_model_with_guardrails(self, user_input):
        """Invoke Bedrock model with guardrail protection"""
        # Apply input guardrail
        input_safe, processed_input = self.apply_input_guardrail(user_input)
        
        if not input_safe:
            return processed_input
        
        # Prepare request for Claude
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": processed_input
                }
            ]
        }
        
        try:
            # Invoke model
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body),
                contentType='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            model_output = response_body['content'][0]['text']
            
            # Apply output guardrail
            output_safe, final_output = self.apply_output_guardrail(model_output)
            
            return final_output
            
        except ClientError as e:
            return f"Error invoking model: {e}"

def main():
    st.title("🛡️ Secure Bedrock Chat Application")
    st.write("This application demonstrates content filtering using Amazon Bedrock Guardrails")
    
    # Configuration
    if 'guardrail_id' not in st.session_state:
        st.session_state.guardrail_id = ""
    
    with st.sidebar:
        st.header("Configuration")
        guardrail_id = st.text_input(
            "Guardrail ID", 
            value=st.session_state.guardrail_id,
            help="Enter your Bedrock Guardrail ID"
        )
        
        guardrail_version = st.selectbox(
            "Guardrail Version",
            ["DRAFT", "1", "2", "3"],
            help="Select the guardrail version to use"
        )
        
        if st.button("Update Configuration"):
            st.session_state.guardrail_id = guardrail_id
            st.success("Configuration updated!")
    
    if not guardrail_id:
        st.warning("Please enter a Guardrail ID in the sidebar to continue.")
        return
    
    # Initialize the secure app
    try:
        app = SecureBedrockApp(guardrail_id, guardrail_version)
    except Exception as e:
        st.error(f"Failed to initialize application: {e}")
        return
    
    # Chat interface
    st.header("💬 Secure Chat")
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Enter your message..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response with guardrails
        with st.chat_message("assistant"):
            with st.spinner("Processing with security checks..."):
                response = app.invoke_model_with_guardrails(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Test scenarios
    st.header("🧪 Test Content Filtering")
    
    test_scenarios = [
        "What is the weather like today?",  # Safe content
        "I hate people from that country",  # Hate speech
        "My email is john@example.com",     # PII
        "You should invest in Bitcoin now", # Financial advice
    ]
    
    selected_test = st.selectbox("Select a test scenario:", test_scenarios)
    
    if st.button("Test Scenario"):
        with st.spinner("Testing..."):
            result = app.invoke_model_with_guardrails(selected_test)
            st.write("**Result:**", result)

if __name__ == "__main__":
    main()