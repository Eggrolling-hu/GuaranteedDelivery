from langchain.vectorstores import Weaviate

from langchain.tools import tool

from core.data import JinaEmbeddings

import weaviate


client = weaviate.Client(
    url="http://localhost:8080",  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key="shadowmotion-secret-key"))

embedding = JinaEmbeddings("127.0.0.1")
db = Weaviate(client=client, embedding=embedding,
              index_name="LangChain", text_key="text", by_text=False)


@tool(return_direct=True)
def jina_retriever(query: str, k: int = 3) -> str:
    """Searches the local vector database for the query."""

    docs = db.similarity_search(query, k=k)

    # print(docs)

    return docs
