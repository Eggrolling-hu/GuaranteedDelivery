from langchain import PromptTemplate

PROMPT = """
你需要扮演一个优秀的意图识别助手，你需要判断人类的问题是属于（闲聊/社保/医疗/法律/物流）类别的一项。
你不需要做任何解释说明，并且严格按照示例的格式进行输出，仅输出["闲聊","社保","医疗","法律","物流"]。

以下是一个示例：
人类：我被车撞了，请问我应该如何向法庭提起诉讼？
AI: 法律

现在开始：
人类：{query}
AI:
"""


def intent_recognition_raw_prompt():
    return PromptTemplate(template=PROMPT, input_variables=["query"])


def intent_recognition_prompt(query: str):
    P = PromptTemplate(template=PROMPT, input_variables=["query"])
    return P.format(query=query)


if __name__ == "__main__":
    print(intent_recognition_prompt("你们的装箱算法能不能用在家居业呀？主要用于是沙发的装箱。"))
