import warnings  # noqa: E501
warnings.filterwarnings('ignore')  # noqa: E501

from typing import Any, List, Mapping, Optional

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM

import zhipuai


class ZhiPuLLM(LLM):
    n: int = 0
    zhipu_api_key: str = ""
    model: str = ""

    def __init__(self, zhipu_api_key: str, model: str = "chatglm_std"):
        super().__init__()
        self.zhipu_api_key = zhipu_api_key
        self.model = model

        zhipuai.api_key = self.zhipu_api_key

    @property
    def _llm_type(self) -> str:
        return "ZhiPuAI"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        # if stop is not None:
        #     raise ValueError("stop kwargs are not permitted.")

        response = zhipuai.model_api.invoke(
            model=self.model,
            prompt=[
                {"role": "user", "content": prompt},
            ]
        )

        generated_text = response['data']["choices"][0]["content"]

        print("response from ZhiPu: {}".format(generated_text))

        print("tokens: {}".format(response['data']["usage"]["total_tokens"]))

        return generated_text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n}


if __name__ == "__main__":
    llm = ZhiPuLLM(
        zhipu_api_key="yourkey",
        model="chatglm_lite")
    print(llm("你好"))
