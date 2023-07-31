import sys  # noqa: E501
sys.path.append('/home/shadowmotion/Documents/code/demo/HRSSC')  # noqa: E501


from langchain.vectorstores import Weaviate
from langchain.schema import Document
from utils import JinaEmbeddings
import weaviate
import os

client = weaviate.Client(
    url="http://localhost:8080",  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key="shadowmotion-secret-key"))

embedding = JinaEmbeddings("127.0.0.1")
db = Weaviate(client=client, embedding=embedding,
              index_name="LangChain_abc", text_key="text", by_text=False)


query_list = [
    "公司的法定代表人是谁",
    "电子邮箱是什么",
    "公司的外文名称是什么",
]

for query in query_list:
    docs = db.similarity_search(query, k=3)

    for e in docs:
        print(e.page_content)
