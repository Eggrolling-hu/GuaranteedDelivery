import warnings  # noqa: E501
warnings.filterwarnings('ignore')  # noqa: E501

from typing import Any, List, Mapping, Optional

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM

from docarray import Document, DocumentArray
from jina import Client


class JinaLLM(LLM):
    n: int = 0
    port: int = 0
    host: str = ""
    client: Any

    def __init__(self, host: str = '0.0.0.0', port: int = 50002):
        super().__init__()
        self.client = Client(host=host, port=port)

    @property
    def _llm_type(self) -> str:
        return "ShadowMotion"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        # if stop is not None:
        #     raise ValueError("stop kwargs are not permitted.")

        response = self.client.post(
            '/', inputs=DocumentArray([Document(text=prompt, tags={"history": []})]))

        return response[0].text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n}


if __name__ == "__main__":
    llm = JinaLLM()
    print(llm("你好"))
