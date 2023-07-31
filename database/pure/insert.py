# import sys  # noqa: E501
# sys.path.append('/home/shadowmotion/Documents/code/demo/HRSSC')  # noqa: E501

from langchain.vectorstores import Weaviate
from ...core.data import JinaEmbeddings
import weaviate

from raw.QA import read_qa_file

client = weaviate.Client(
    url="http://localhost:8080",  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key="shadowmotion-secret-key"))

embedding = JinaEmbeddings()
db = Weaviate(client=client, embedding=embedding,
              index_name="LangChain", text_key="text", by_text=False)


# print(read_qa_file("raw/QA.txt"))

db.add_texts(texts=read_qa_file("./raw/QA.txt"))

# db.add_documents(
#     [Document(page_content="1", metadata={"Q": "1+1=", "A": "2"})]
# )
