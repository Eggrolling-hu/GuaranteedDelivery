import sys  # noqa: E501
sys.path.append('/home/shadowmotion/Documents/code/demo/HRSSC')  # noqa: E501


from core.data import JinaEmbeddings
from langchain.vectorstores import Weaviate
from langchain.schema import Document
import weaviate
import os

client = weaviate.Client(
    url="http://localhost:8080",  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key="shadowmotion-secret-key"))

embedding = JinaEmbeddings()
db = Weaviate(client=client, embedding=embedding,
              index_name="LangChain", text_key="text", by_text=False)


query = "我有一个服装厂，可以用你们的装箱算法吗"
docs = db.similarity_search(query, k=3)

for e in docs:
    print(e)
