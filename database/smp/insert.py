# import sys  # noqa: E501
# sys.path.append('/home/shadowmotion/Documents/code/demo/HRSSC')  # noqa: E501

from langchain.vectorstores import Weaviate
from utils import JinaEmbeddings
from jina import Document
import weaviate
import glob
import os


client = weaviate.Client(
    url="http://localhost:8080",  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key="shadowmotion-secret-key"))

embedding = JinaEmbeddings("127.0.0.1")


# print(embedding.embed_documents(read_qa_file("raw/QA.txt")))


def insert_txt(path):

    basename = os.path.basename(path).split('.')[0].replace('_', "")
    basename = 55050666276407657353454500445892807833

    db = Weaviate(client=client, embedding=embedding,
                  index_name=f"LangChain_{basename}", text_key="text", by_text=False)
    texts = []

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i > 0 and i % 1000 == 0:
                db.add_texts(texts=texts)
                print(f"表格数据已注入{i}")
                texts = []
            if len(line) <= 1:
                continue
            texts.append(line[:-1])
        db.add_texts(texts=texts)
        print(f"表格数据已注入{i}")
        texts = []
        print(db._index_name)


def insert_table(path):
    basename = os.path.basename(path).split('.')[0]

    db = Weaviate(client=client, embedding=embedding,
                  index_name=f"LangChain_{basename}", text_key="text", by_text=False)

    texts = []

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i > 0 and i % 1000 == 0:
                db.add_texts(texts=texts)
                print(f"文字数据已注入{i}")
                texts = []
            if len(line) <= 1:
                continue
            texts.append(line[:-1])
        db.add_texts(texts=texts)
        print(f"文字数据已注入{i}")
        texts = []


if __name__ == "__main__":
    base_tokenizer_model = 'D:\\code\\llm\\embeding\\text2vec-base-chinese-paraphrase'
    TXT_DIRECTORY = "../../data/chatglm_llm_fintech_raw_dataset/alldata"
    file_names = glob.glob(TXT_DIRECTORY + '/*')

    for file_name in file_names:
        insert_txt(file_name)
