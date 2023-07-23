from langchain import PromptTemplate

PROMPT = """
你需要扮演一个优秀的实体识别助手。你需要判断人类的对话中包含的实体（人名/地名/应用场景）内容。
请依据具体问题内容，识别并输出最合适的应用场景选项["化工业", "服装业", "旅游业", "电器业", "其他"]。
如果信息未包含对应实体，请输出"无"。

注意：你不需要做任何解释说明，仅严格按照示例的格式进行输出。

以下是一个示例：
人类：我有一个服装厂，是否可以应用你们的装箱算法改善装载率呢？
AI: 人名：无 地名：无 应用场景：服装业

现在开始，接着回答：
人类：{query}
AI:
"""


def entity_recognition_raw_prompt():
    return PromptTemplate(template=PROMPT, input_variables=["query"])


def entity_recognition_prompt(query: str):
    P = PromptTemplate(template=PROMPT, input_variables=["query"])
    return P.format(query=query)


if __name__ == "__main__":
    print(entity_recognition_prompt("你们的装箱算法能不能用在家居业呀？主要用于是沙发的装箱。"))
