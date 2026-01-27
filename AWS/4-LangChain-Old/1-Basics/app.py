import os
from dotenv import load_dotenv
import streamlit as st
# from langchain_aws import BedrockLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_aws import ChatBedrock

# Load environment variables
load_dotenv()

# Configure AWS credentials and region

# Disable Langsmith tracking to avoid SSL issues
os.environ["LANGCHAIN_TRACING_V2"] = "false"

# Initialize Bedrock client
llm = ChatBedrock(
    model_id="amazon.nova-pro-v1:0",
    region_name="us-east-1"
)

# Prompt Template
prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful assistant. Please respond to the following query: {question}"
)

# Create LLMChain
chain = prompt | llm

# Streamlit framework
st.title('Langchain Demo With Amazon Bedrock')
input_text = st.text_input("Search the topic you want")

if input_text:
    response = chain.invoke(input_text)
    st.write(response)
