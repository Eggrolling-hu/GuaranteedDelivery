from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.llms import OpenAI

from core.chain.retrieval_qa import MyCustomChain
from core import ShadowMotion
from core.llm import JinaLLM

if __name__ == "__main__":
    # sm = ShadowMotion(llm="OpenAI")

    # respond = sm.run("客户在装箱过程中通常遇到哪些问题和痛点？")

    # print(respond)

    llm = JinaLLM(host="0.0.0.0", port=50002)

    # openai_api_key = "yourkey"

    # llm = OpenAI(openai_api_key=openai_api_key,
    #              openai_proxy="socks5://127.0.0.1:7891",
    #              max_tokens=2048)

    chain = MyCustomChain(llm=llm)

    # chain.run(query="你们公司的装箱算法可以用在服装业吗",
    #           callbacks=[StdOutCallbackHandler()])

    while True:
        print("请输入你的问题:")
        query = input()
        chain.run(query=query,
                  callbacks=[StdOutCallbackHandler()])
