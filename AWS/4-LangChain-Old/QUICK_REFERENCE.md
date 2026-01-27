# Quick Migration Reference Card

## Status: 10/25 Complete (40%)

## Next Files to Migrate (In Order)
1. `2-Components/2-Selectors/1-example_selectors.ipynb`
2. `2-Components/2-Selectors/2-example_selectors_length_based.ipynb`
3. `2-Components/2-Selectors/4-example_selectors_ngram.ipynb`
4. `2-Components/2-Selectors/5-example_selectors_mmr.ipynb`
5. `2-Components/3-ChatModels/2-chat_model_caching.ipynb`

## Search & Replace Patterns

### 1. ChatOpenAI Import
**Find:** `from langchain_openai import ChatOpenAI`
**Replace:** `from langchain_aws import ChatBedrock`

### 2. ChatOpenAI Instance
**Find:** `ChatOpenAI(model="gpt-4")`
**Replace:** `ChatBedrock(model_id="us.amazon.nova-pro-v1:0")`

**Find:** `ChatOpenAI(model="gpt-3.5-turbo")`
**Replace:** `ChatBedrock(model_id="us.amazon.nova-pro-v1:0")`

**Find:** `ChatOpenAI(model="gpt-4o-mini")`
**Replace:** `ChatBedrock(model_id="us.amazon.nova-pro-v1:0")`

### 3. OpenAIEmbeddings Import
**Find:** `from langchain_openai import OpenAIEmbeddings`
**Replace:** `from langchain_aws import BedrockEmbeddings`

### 4. OpenAIEmbeddings Instance
**Find:** `OpenAIEmbeddings()`
**Replace:** `BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")`

### 5. Legacy OpenAI Import
**Find:** `from langchain_openai import OpenAI`
**Replace:** `from langchain_aws import ChatBedrock`

### 6. Remove API Key Setup
**Find:** `os.environ["OPENAI_API_KEY"] = getpass()`
**Replace:** `# AWS credentials configured via AWS CLI`

### 7. Remove Callback Manager
**Find:** `from langchain_community.callbacks.manager import get_openai_callback`
**Replace:** `# Bedrock doesn't have equivalent callback manager`

## Model IDs
- **LLM:** `us.amazon.nova-pro-v1:0`
- **Embeddings:** `amazon.titan-embed-text-v2:0`

## Files to Check
```bash
cd /home/ramakrishna/Code/GenAI-for-Dev-Course/AWS/4-LangChain
cat MIGRATION_PROGRESS.md
```
