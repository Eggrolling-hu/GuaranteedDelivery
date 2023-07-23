from langchain import PromptTemplate

PROMPT = """
你需要扮演一个优秀的客服。你需要根据提供的对话记录以及额外信息回答人类的问题。

回答要简练，清晰，准确。多参考额外信息。

现在开始：

历史对话：{history}
意图识别：{intent}
实体提取：{entity}
关键信息：{key_information}
额外信息：{extra_information}

人类：{query}
AI:
"""


def answer_generation_raw_prompt():
    return PromptTemplate(template=PROMPT, input_variables=["history", "intent", "entity", "key_information", "extra_information", "query"])


def answer_generation_prompt(query: str):
    P = PromptTemplate(template=PROMPT, input_variables=[
                       "history", "intent", "entity", "key_information", "extra_information", "query"])
    return P.format(query=query)


if __name__ == "__main__":
    print(answer_generation_prompt("你们公司的装箱算法可以用在服装业吗"))
