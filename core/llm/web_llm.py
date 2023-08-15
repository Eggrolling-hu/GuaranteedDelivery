

from docarray import Document, DocumentArray
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Mapping, Optional
import requests
import json


print()

import warnings  # noqa: E501
warnings.filterwarnings('ignore')  # noqa: E501


class WebLLM(LLM):
    n: int = 0
    token: str = ""
    url: str = ""
    client: Any

    def __init__(
            self,
            url: str = 'http://quickstart-20230815-iv6e.1059534654016236.cn-shanghai.pai-eas.aliyuncs.com/',
            token: str = 'MTI1YTliMTI0YmQ3MTIyOWY3ZmRiMDk5ZDZiODZiZjliN2RlMzZjMg=='):
        super().__init__()
        self.url = url
        self.token = token

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
        request_body = {
            "data": {
                "query": f"{prompt}",
                "history": [],
                "max_length": 2048
            }
        }

        headers = {"Authorization": self.token}
        resp = requests.post(url=self.url, headers=headers, json=request_body)

        response = json.loads(resp.content.decode())

        return response["response"]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n}


if __name__ == "__main__":
    llm = WebLLM()
    print(llm("你好"))
