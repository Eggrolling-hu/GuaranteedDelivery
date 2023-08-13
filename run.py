
from core.data import JinaEmbeddings
from core.chain.smp import run

from langchain.vectorstores import Weaviate
from elasticsearch import Elasticsearch

import jsonlines
import weaviate
import json
import os

from datetime import datetime


if __name__ == "__main__":
    # -> Init Embedding Database
    embedding = JinaEmbeddings("127.0.0.1")
    client = weaviate.Client(
        url="http://localhost:8080",  # Replace with your endpoint
        auth_client_secret=weaviate.AuthApiKey(api_key="shadowmotion-secret-key"))

    # -> Init Embedding Database
    es = Elasticsearch('http://localhost:50004')

    # -> Init UUID Dict
    with open("./data/chatglm_llm_fintech_raw_dataset/uuid.json", "r") as f:
        uuid_dict = json.load(f)

    # -> Init crawl Dict
    with open("./data/test_temp/all_crawl.json", "r") as f:
        crawl_dict = json.load(f)
    with open("./data/test_temp/name_map_crawl.json", "r") as f:
        crawl_name_dict = json.load(f)

    # question = "平安银行在2020年对联营企业和合营企业的投资收益是多少元？"

    questions_array = []

    with jsonlines.open('./data/chatglm_llm_fintech_raw_dataset/test_questions.jsonl', 'r') as reader:
        for obj in reader:
            questions_array.append(obj)

    # Define skip and max files
    questions_array = questions_array[:10]

    current_time = datetime.now()

    formatted_time = current_time.strftime('%Y-%m-%d_%H-%M-%S')

    if not os.path.exists("./data/logs"):
        os.mkdir("./data/logs")
    if not os.path.exists("./data/submit"):
        os.mkdir("./data/submit")

    with open(f"./data/logs/{formatted_time}.txt", "w") as f:
        for i, item in enumerate(questions_array):
            question = item['question']
            answer = run(question, uuid_dict, crawl_dict,
                         crawl_name_dict, es, f)
            item["answer"] = answer

            with open(f"./data/submit/{formatted_time}.jsonl", "w") as file:
                line = json.dumps(item, ensure_ascii=False)
                line = line.replace('\\n', '')
                file.write(line + '\n')
