import os
from dotenv import load_dotenv
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import VectorStoreIndex


def ragllm():
    documents = SimpleWebPageReader(html_to_text=True).load_data(["https://paulgraham.com/worked.html"])
    print(documents[0].text)
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    response = query_engine.query("What is this page about?")
    print(response)
    pass
if __name__ == '__main__' :
    load_dotenv()
    ragllm()