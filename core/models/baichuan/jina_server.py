import warnings  # noqa: E501
warnings.filterwarnings('ignore')  # noqa: E501

from jina import DocumentArray, Executor, requests, Flow
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from typing import Dict, Tuple, Union, Optional
from torch.nn import Module

import logging
import torch
import json
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"


class BaiChuan(Executor):
    def __init__(
            self,
            model_name: str = '',
            lora_path: str = '',
            device: str = None,
            num_gpus: int = 0,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.shadowmotion = {}
        # # 定义你想在每个GPU上分配的显存大小（以字节为单位）
        memory_size = 4 * 1024**3  # 2GB
        # 计算每个元素的大小（浮点数通常是4字节）
        element_size = torch.cuda.FloatTensor().element_size()  # 4 bytes
        # 计算你需要多少个浮点数来填充2GB的显存
        n_elements = memory_size // element_size

        # 创建一个列表来保存每个GPU上创建的张量
        block_mem_tensors = []

        # 在每个GPU上创建一个浮点张量
        for i in range(0, 1):
            torch.cuda.set_device(i)
            tensor = torch.cuda.FloatTensor(int(n_elements)).fill_(0)
            block_mem_tensors.append(tensor)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        self.model.generation_config = GenerationConfig.from_pretrained(
            model_name
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            use_fast=False,
            trust_remote_code=True
        )

        # # 删除存储在block_mem_tensors中的每个张量
        for tensor in block_mem_tensors:
            del tensor

        # 清空block_mem_tensors列表
        block_mem_tensors.clear()

        # 释放所有未使用的缓存
        torch.cuda.empty_cache()

    @requests
    def chat(self, docs: DocumentArray, pre_history: bool = False, **kwargs):
        for doc in docs:
            prompt = doc.text
            history = doc.tags.get('history', [])

            print('---------prompt----------')

            print(prompt)
            messages = []
            messages.append({"role": "user", "content": prompt})

            response = self.model.chat(self.tokenizer, messages)

            doc.text = response
            doc.tags['history'] = json.dumps(history, ensure_ascii=False)

            print('--------response---------')

            print(response)

            print('----------end------------')


if __name__ == "__main__":
    model_name = "/media/shadowmotion/0CD113590CD11359/code/llm/baichuan/baichuan-13b-chat"
    # lora_path = 'lora'
    lora_path = ''
    port = 50002

    f = Flow(port=port).add(
        uses=BaiChuan,
        uses_with={
            'model_name': model_name,
            'lora_path': lora_path,
            'device': 'cuda',
            'num_gpus': 4,
        },
        gpus='device=0,device=1,device=2,device=3',
    )

    with f:
        # start server, backend server forever
        f.block()
