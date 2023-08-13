from core.models.chatglm2.jina_client import encode
from core.prompt import intent_recognition_prompt
from core.prompt import entity_recognition_prompt
from core.prompt import answer_generation_prompt
from core.data import JinaEmbeddings

from langchain.vectorstores import Weaviate
from elasticsearch import Elasticsearch

import weaviate
import json


def parse_entity_recognition(response: str):
    parse_list = []
    lines = response.split('\n')
    for line in lines:
        sep = ':' if ':' in lines[-1] else '：'
        if "公司名" in line:
            parse_list.append(line.split(sep)[1])
        if "年份" in line:
            parse_list.append(line.split(sep)[1])
    return parse_list


def parse_intent_recognition(response: str):
    lines = response.split('\n')
    return lines[-1]


def attain_uuid(entities, uuid_dict):
    for k, v in uuid_dict.items():
        fg = True
        for entity in entities:
            if entity not in k:
                fg = False
                break
        if fg:
            print(entities, k)
            return v, k
    return None, None


def run(question, uuid_dict, crawl_dict, crawl_name_dict, es, f, qa_list=[]):
    f.write("= = 流程开始 = = \n")
    f.write(f"Q:\n{question}\n\n")

    # -> Intent Recognition
    f.write("= = 意图识别 = = \n")
    prompt = intent_recognition_prompt(question)
    response = encode(prompt, history=[])
    f.write(f"R:\n{response[0].text}\n\n")

    if "检索问题" not in parse_intent_recognition(response[0].text):
        f.write("开放问题直接作答\n")
        response = encode(question, history=[])
        answer = response[0].text
        f.write(f"R:\n{answer}\n\n")
        return answer

    # -> Entity Recognition
    f.write("= = 实体提取 = = \n")
    prompt = entity_recognition_prompt(question)
    response = encode(prompt, history=[])
    f.write(f"R:\n{response[0].text}\n\n")
    entities = parse_entity_recognition(response[0].text)
    uuid, file_name = attain_uuid(entities, uuid_dict)
    f.write(f"R:\n{uuid}\n\n")
    if not uuid and entities[0][0] == '年':
        entities[0] = entities[0][1:]
        uuid, file_name = attain_uuid(entities, uuid_dict)
        f.write(f"R:\n fixed company name {entities[0]}\n\n")

    if not uuid:
        f.write("未知公司不予作答\n")
        return ""

    elastic_search_success = False
    extra_information_list = []

    # -> ElasticSearch
    f.write("= = ElasticSearch = = \n")
    index_name = f"{uuid}"
    index_name = "all_property"
    try:
        for word in entities:
            replaced_question = question.replace(word, '')

        search_query = {
            "query": {
                "match": {
                    "text": replaced_question
                }
            }
        }

        search_resp = es.search(index=index_name, body=search_query)

        docs = search_resp["hits"]["hits"][:50]

        n = 0
        for i, e in enumerate(docs):
            try:
                property_name = e['_source']['text']
                company = crawl_name_dict[file_name]
                year = file_name.split("__")[4]+"报"
                property_value = crawl_dict[company][year][property_name]
                if not property_value or property_value in ["None", "null"]:
                    continue
                f.write(
                    f"ES: = = = = = = = = = = = k[{n}] = = = = = = = = = = =\n")
                f.write(e['_source']['text'])
                f.write("\n")
            except:
                continue
            extra_information_list.append(f"{property_name}是{property_value}")
            n += 1
            if n > 3:
                break
    except:
        f.write("数据库暂未录入\n")

    # -> Embedding Database
    f.write("= = EmbeddingDatabase = = \n")
    if not elastic_search_success and not extra_information_list:
        index_name = f"LangChain_{uuid}"
        try:
            db = Weaviate(client=client, embedding=embedding,
                          index_name=index_name, text_key="text", by_text=False)

            for word in entities:
                replaced_question = question.replace(word, '')

            docs = db.similarity_search(replaced_question, k=5)

            for i, e in enumerate(docs):
                f.write(
                    f"ED: = = = = = = = = = = = k[{i}] = = = = = = = = = = =\n")
                f.write(e.page_content)
                f.write("\n")
                extra_information_list.append(e.page_content)
        except:
            f.write("数据库暂未录入\n")

        response = encode(question, history=[])
        answer = response[0].text

    f.write("= = AnswerGeneration = = \n")
    extra_information = "\n".join(extra_information_list)
    f.write(extra_information+'\n')
    prompt = answer_generation_prompt(extra_information, question)
    response = encode(prompt, history=[])
    f.write(f"R:\n{response[0].text}\n\n")
    answer = response[0].text
    return answer


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

    question = "本钢板材在2020年对联营企业和合营企业的投资收益是多少元？"

    with open("./data/test_temp/main_log.txt", "w") as f:
        run(question, uuid_dict, crawl_dict, crawl_name_dict, es, f)
