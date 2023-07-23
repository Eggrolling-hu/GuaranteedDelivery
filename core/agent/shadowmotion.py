from langchain.agents import AgentType
from langchain.llms import OpenAI

from langchain.agents import initialize_agent

from core.llm import JinaLLM, ZhiPuLLM

from core.tool import jina_retriever


class ShadowMotion:
    def __init__(self, llm="LocalLLM") -> None:
        if llm == "LocalLLM":
            llm = JinaLLM(host="0.0.0.0", port=50003)
        elif llm == "ZhiPu":
            llm = ZhiPuLLM(
                zhipu_api_key="yourkey")
        elif llm == "OpenAI":
            llm = OpenAI(openai_api_key="yourkey",
                         openai_proxy="socks5://127.0.0.1:7891")
        else:
            raise ValueError("Error LLM Type.")

        tools = [jina_retriever,]

        self.agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    def run(self, query: str):
        return self.agent.run(query)
