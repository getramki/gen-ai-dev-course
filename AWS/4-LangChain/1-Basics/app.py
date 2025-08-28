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

# Langsmith tracking (if you still want to use it)
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Initialize Bedrock client
llm = ChatBedrock(
    model_id="amazon.nova-lite-v1:0"
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
