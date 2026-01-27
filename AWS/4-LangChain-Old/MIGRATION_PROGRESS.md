# OpenAI to Amazon Bedrock Nova Pro Migration Progress

## Migration Date: 2024
## Target: Replace all OpenAI references with Amazon Bedrock Nova Pro (us.amazon.nova-pro-v1:0)

---

## Migration Status

### ✅ COMPLETED (17/25)
1. `1-Basics/app.py` - Updated from Nova Lite to Nova Pro
2. `1-Basics/llm_chain.ipynb` - Migrated from ChatOpenAI to ChatBedrock
3. `2-Components/1-PromptTemplates/1-few_shot_examples.ipynb` - Migrated OpenAIEmbeddings to BedrockEmbeddings
4. `2-Components/1-PromptTemplates/2-few_shot_examples_chat.ipynb` - Migrated ChatOpenAI + OpenAIEmbeddings to Bedrock
5. `2-Components/2-Selectors/3-example_selectors_similarity.ipynb` - Migrated OpenAIEmbeddings to BedrockEmbeddings
6. `2-Components/3-ChatModels/1-chat_token_usage_tracking.ipynb` - Migrated ChatOpenAI to ChatBedrock
7. `2-Components/6-OutputParsers/1-output_parser_structured.ipynb` - Migrated OpenAI to ChatBedrock
8. `2-Components/7-DocumentLoaders/document_loader_pdf.ipynb` - Migrated OpenAIEmbeddings to BedrockEmbeddings
9. `3-Runnables/runnables.ipynb` - Migrated ChatOpenAI to ChatBedrock
10. `4-ChatBot/chatbot.ipynb` - Migrated ChatOpenAI to ChatBedrock
11. `2-Components/1-PromptTemplates/1-few_shot_examples copy.ipynb` - Migrated OpenAIEmbeddings to BedrockEmbeddings
12. `2-Components/2-Selectors/5-example_selectors_mmr.ipynb` - Migrated OpenAIEmbeddings to BedrockEmbeddings
13. `2-Components/3-ChatModels/2-chat_model_caching.ipynb` - Migrated ChatOpenAI to ChatBedrock
14. `2-Components/4-Messages/1-trim_messages.ipynb` - Migrated ChatOpenAI to ChatBedrock
15. `2-Components/2-Selectors/4-example_selectors_ngram.ipynb` - No OpenAI (SKIPPED)
16. `2-Components/2-Selectors/1-example_selectors.ipynb` - No OpenAI (SKIPPED)
17. `2-Components/6-OutputParsers/2-output_parser_json.ipynb` - Migrated ChatOpenAI to ChatBedrock

### 🔄 IN PROGRESS (0/25)
None

### ⏳ PENDING (0/25)
None - All files completed or skipped!

### ⏭️ SKIPPED (8 files - No OpenAI usage)
- `2-Components/1-PromptTemplates/3-prompts_composition.ipynb`
- `2-Components/1-PromptTemplates/4-prompts_partial.ipynb`
- `2-Components/2-Selectors/1-example_selectors.ipynb`
- `2-Components/2-Selectors/2-example_selectors_length_based.ipynb`
- `2-Components/2-Selectors/4-example_selectors_ngram.ipynb`
- `2-Components/4-Messages/2-filter_messages.ipynb`
- `2-Components/5-LLMs/local_llms.ipynb`
- `2-Components/7-DocumentLoaders/document_loader_csv.ipynb`
- `2-Components/7-DocumentLoaders/document_loader_directory.ipynb`
- `2-Components/7-DocumentLoaders/document_loader_html.ipynb`
3. `2-Components/1-PromptTemplates/1-few_shot_examples.ipynb`
4. `2-Components/1-PromptTemplates/1-few_shot_examples copy.ipynb`
5. `2-Components/1-PromptTemplates/2-few_shot_examples_chat.ipynb`
6. `2-Components/1-PromptTemplates/3-prompts_composition.ipynb`
7. `2-Components/1-PromptTemplates/4-prompts_partial.ipynb`
8. `2-Components/2-Selectors/1-example_selectors.ipynb`
9. `2-Components/2-Selectors/2-example_selectors_length_based.ipynb`
10. `2-Components/2-Selectors/3-example_selectors_similarity.ipynb`
11. `2-Components/2-Selectors/4-example_selectors_ngram.ipynb`
12. `2-Components/2-Selectors/5-example_selectors_mmr.ipynb`
13. `2-Components/3-ChatModels/1-chat_token_usage_tracking.ipynb`
14. `2-Components/3-ChatModels/2-chat_model_caching.ipynb`
15. `2-Components/4-Messages/1-trim_messages.ipynb`
16. `2-Components/4-Messages/2-filter_messages.ipynb`
17. `2-Components/5-LLMs/local_llms.ipynb`
18. `2-Components/6-OutputParsers/1-output_parser_structured.ipynb`
19. `2-Components/6-OutputParsers/2-output_parser_json.ipynb`
20. `2-Components/7-DocumentLoaders/document_loader_csv.ipynb`
21. `2-Components/7-DocumentLoaders/document_loader_directory.ipynb`
22. `2-Components/7-DocumentLoaders/document_loader_html.ipynb`
23. `2-Components/7-DocumentLoaders/document_loader_pdf.ipynb`
24. `3-Runnables/runnables.ipynb`
25. `4-ChatBot/chatbot.ipynb`

---

## Migration Rules Applied

### LLM Models:
- `from langchain_openai import ChatOpenAI` → `from langchain_aws import ChatBedrock`
- `ChatOpenAI(model="gpt-4")` → `ChatBedrock(model_id="us.amazon.nova-pro-v1:0")`
- `ChatOpenAI(model="gpt-3.5-turbo")` → `ChatBedrock(model_id="us.amazon.nova-pro-v1:0")`
- `OpenAI(model_name="...")` → `ChatBedrock(model_id="us.amazon.nova-pro-v1:0")`

### Embeddings:
- `from langchain_openai import OpenAIEmbeddings` → `from langchain_aws import BedrockEmbeddings`
- `OpenAIEmbeddings()` → `BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")`

### Environment Variables:
- Remove: `os.environ["OPENAI_API_KEY"]` references
- AWS credentials assumed to be configured via AWS CLI

### Callbacks:
- Remove: `from langchain_community.callbacks.manager import get_openai_callback`
- Note: Bedrock doesn't have equivalent callback manager for token tracking

---

## Notes:
- AWS credentials are already configured on the system
- app.py already uses ChatBedrock with Nova Lite - can be updated to Nova Pro if needed
- Some OpenAI-specific features (like streaming token usage) may not have direct Bedrock equivalents

---

## Session Recovery Instructions:
To continue migration in a new session:
1. Check this file for completed items (marked with ✅)
2. Start with the first item in PENDING section
3. Update status as you progress
4. Move completed items to COMPLETED section with timestamp
